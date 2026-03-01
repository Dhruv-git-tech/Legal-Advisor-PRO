from flask import Flask, render_template, request, jsonify, send_file, session
from pdf_extractor import extract_text_from_pdfs, load_extracted_data
from nlp_model import LegalCaseMatcher
from summarizer import LegalCaseSummarizer
from ai_analyzer import LegalAIAnalyzer
from legal_chatbot import LegalChatbot
from document_drafter import DocumentDrafter
from legal_ner import LegalNER
from ipc_lookup import IPCLookup
from database import Database
import os
import uuid

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'legal-ai-secret-key-2024')

# Global instances
model = None
summarizer = None
ai_analyzer = None
chatbot = None
drafter = None
ner = None
ipc = None
db = None

def initialize_app():
    """Initialize all modules on startup"""
    global model, summarizer, ai_analyzer, chatbot, drafter, ner, ipc, db
    
    try:
        # Initialize database
        db = Database()
        print("✓ Database initialized.")
        
        # Initialize summarizer
        summarizer = LegalCaseSummarizer()
        print("✓ Summarizer initialized.")
        
        # Initialize AI analyzer (Gemini/Groq)
        ai_analyzer = LegalAIAnalyzer()
        providers = ai_analyzer.get_provider_info()
        if providers:
            print(f"✓ AI Analyzer initialized: {', '.join(providers)}")
        else:
            print("⚠ AI Analyzer: No API keys configured. Set GEMINI_API_KEY or GROQ_API_KEY.")
        
        # Initialize chatbot
        chatbot = LegalChatbot()
        print("✓ Legal Chatbot initialized.")
        
        # Initialize document drafter
        drafter = DocumentDrafter()
        print("✓ Document Drafter initialized.")
        
        # Initialize NER
        ner = LegalNER()
        if ner.is_available():
            print("✓ Legal NER initialized with spaCy.")
        else:
            print("⚠ Legal NER: Using regex fallback (install spacy + model for full NER).")
        
        # Initialize IPC lookup
        ipc = IPCLookup()
        print(f"✓ IPC Lookup initialized: {len(ipc.sections)} sections loaded.")
        
        # Load NLP model for case matching
        dataset_path = 'Dataset'
        if os.path.exists('extracted_data.pkl'):
            print("Loading cached case data...")
            texts, filenames = load_extracted_data()
        else:
            print("Extracting text from PDFs... This may take a while.")
            texts, filenames = extract_text_from_pdfs(dataset_path)
        
        print("Training TF-IDF model...")
        model = LegalCaseMatcher()
        model.train(texts, filenames)
        print(f"✓ Model loaded: {len(filenames)} cases indexed.")
        
        print("\n" + "=" * 50)
        print("  LegalAI Assistant — All Systems Ready")
        print("=" * 50 + "\n")
        
    except Exception as e:
        print(f"✗ Initialization error: {e}")
        import traceback
        traceback.print_exc()

# Initialize when app starts
initialize_app()


# ============================================
# PAGE ROUTES
# ============================================

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    stats = db.get_stats() if db else {'total_searches': 0, 'total_chats': 0, 'total_documents': 0}
    return render_template('dashboard.html', stats=stats)

@app.route('/search')
def search_page():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot_page():
    # Generate session ID for chat
    if 'chat_session_id' not in session:
        session['chat_session_id'] = str(uuid.uuid4())
    suggested = chatbot.get_suggested_prompts() if chatbot else []
    return render_template('chatbot.html', suggested_prompts=suggested)

@app.route('/drafter')
def drafter_page():
    doc_types = drafter.get_document_types() if drafter else {}
    return render_template('drafter.html', document_types=doc_types)

@app.route('/ipc-lookup')
def ipc_page():
    categories = ipc.get_all_categories() if ipc else {}
    return render_template('ipc_lookup.html', categories=categories)


# ============================================
# API ROUTES
# ============================================

@app.route('/pdf/<filename>')
def get_pdf(filename):
    """Serve PDF files from the Dataset folder"""
    try:
        pdf_path = os.path.join('Dataset', filename)
        if os.path.exists(pdf_path):
            return send_file(pdf_path, mimetype='application/pdf')
        return jsonify({'error': 'PDF not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['POST'])
def search_cases():
    """Find similar cases based on case study input"""
    try:
        data = request.json
        case_study = data.get('case_study', '')
        
        if not case_study:
            return jsonify({'error': 'No case study provided'}), 400
        if model is None:
            return jsonify({'error': 'Model not loaded. Please reload the application.'}), 500
        
        # Summarize for better matching
        summarized_case = summarizer.summarize_case_study(case_study, max_sentences=3) if summarizer else case_study
        
        # Find similar cases
        results = model.find_similar_cases(summarized_case, top_n=5)
        
        # Extract entities from query
        entities = None
        if ner:
            entities = ner.extract_entities(case_study)
        
        # Get AI analysis
        ai_analysis = None
        if ai_analyzer and ai_analyzer.is_available():
            ai_analysis = ai_analyzer.analyze_case(case_study, results)
        
        # Save to database
        if db:
            db.save_search(case_study, summarized_case, results, ai_analysis)
        
        return jsonify({
            'results': results,
            'original_summary': case_study,
            'summarized_input': summarized_case,
            'ai_analysis': ai_analysis,
            'entities': entities
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Legal chatbot conversation endpoint"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        if not chatbot:
            return jsonify({'error': 'Chatbot not initialized'}), 500
        
        result = chatbot.chat(session_id, message)
        
        # Save to database
        if db and result.get('success'):
            db.save_chat_message(session_id, 'user', message)
            db.save_chat_message(session_id, 'assistant', result['response'], result.get('provider'))
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/draft', methods=['POST'])
def draft_document():
    """Legal document drafting endpoint"""
    try:
        data = request.json
        doc_type = data.get('doc_type', '')
        details = data.get('details', {})
        
        if not doc_type:
            return jsonify({'error': 'No document type specified'}), 400
        if not drafter:
            return jsonify({'error': 'Drafter not initialized'}), 500
        
        result = drafter.draft_document(doc_type, details)
        
        # Save to database
        if db and result.get('success'):
            db.save_document(doc_type, details, result['document'], result.get('provider'))
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/draft/types', methods=['GET'])
def get_document_types():
    """Get available document types"""
    if drafter:
        return jsonify(drafter.get_document_types())
    return jsonify({}), 500


@app.route('/api/ipc-lookup', methods=['GET'])
def ipc_search():
    """Search IPC sections"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    if not ipc:
        return jsonify({'error': 'IPC lookup not initialized'}), 500
    
    results = ipc.search(query)
    return jsonify({'results': results, 'query': query})


@app.route('/api/ipc-suggest', methods=['POST'])
def ipc_suggest():
    """Suggest IPC sections from case description"""
    data = request.json
    description = data.get('description', '').strip()
    if not description:
        return jsonify({'error': 'No description provided'}), 400
    if not ipc:
        return jsonify({'error': 'IPC lookup not initialized'}), 500
    
    results = ipc.suggest_sections(description)
    return jsonify({'suggestions': results})


@app.route('/api/ner', methods=['POST'])
def extract_entities():
    """Extract named entities from legal text"""
    data = request.json
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    if not ner:
        return jsonify({'error': 'NER not initialized'}), 500
    
    result = ner.extract_entities(text)
    return jsonify(result)


@app.route('/api/summarize', methods=['POST'])
def summarize_text():
    """Summarize case text"""
    try:
        data = request.json
        text = data.get('text', '')
        use_llm = data.get('use_llm', False)
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        if summarizer is None:
            return jsonify({'error': 'Summarizer not initialized'}), 500
        
        summary = summarizer.summarize(text, max_sentences=5, use_llm=use_llm)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get usage statistics"""
    if db:
        return jsonify(db.get_stats())
    return jsonify({'total_searches': 0, 'total_chats': 0, 'total_documents': 0})


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get search history"""
    if db:
        history = db.get_search_history(limit=10)
        return jsonify({'history': history})
    return jsonify({'history': []})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
