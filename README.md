# ⚖ LegalAI — AI-Powered Legal Assistant

An intelligent legal assistant that combines **Natural Language Processing (NLP)**, **Large Language Models (LLMs)**, and **Machine Learning** to provide comprehensive legal support for Indian law. Built as a CSE major project demonstrating the integration of modern AI technologies in legal technology.

## 🌟 Key Features

| Module | Technology | Description |
|--------|-----------|-------------|
| 🔍 **Case Search** | TF-IDF + Cosine Similarity | Find similar cases from 400+ indexed legal documents |
| 🤖 **AI Verdict Prediction** | Google Gemini / Groq LLM | Predict case outcomes with confidence scores |
| 💬 **Legal Chatbot** | LLM + Session Memory | Conversational Q&A about Indian law |
| � **Document Drafter** | LLM + Templates | Auto-generate FIRs, notices, complaints, bail apps |
| 📖 **IPC/BNS Lookup** | Searchable Database | 47+ IPC sections with BNS equivalents |
| 🏷️ **Legal NER** | spaCy + EntityRuler | Extract courts, acts, sections, persons from text |

## 🏗 Architecture

```
┌───────────────────────────────────────────┐
│              Frontend (Dark UI)           │
│  Landing │ Dashboard │ Search │ Chatbot   │
│  Drafter │ IPC Lookup                     │
├───────────────────────────────────────────┤
│              Flask Backend                │
├─────────┬─────────┬─────────┬─────────────┤
│ AI      │ Legal   │ Doc     │ IPC         │
│Analyzer │Chatbot  │Drafter  │ Lookup      │
├─────────┼─────────┼─────────┼─────────────┤
│ NLP     │ Legal   │Summa-   │ Database    │
│ Model   │ NER     │rizer    │ (SQLite)    │
├─────────┴─────────┴─────────┴─────────────┤
│         External AI Providers             │
│    Google Gemini  │  Groq (Fallback)      │
└───────────────────────────────────────────┘
```

## 🛠 Technology Stack

- **Backend**: Python, Flask
- **LLM**: Google Gemini 2.0 Flash (primary), Groq Llama 3.3 70B (fallback)
- **NLP**: spaCy (NER, EntityRuler), scikit-learn (TF-IDF), cosine similarity
- **Summarization**: Hybrid extractive (word frequency + legal boosting) + LLM abstractive
- **Database**: SQLite (search history, chat logs, drafted documents)
- **PDF Processing**: PyPDF2
- **Frontend**: HTML5, CSS3 (dark legal theme), vanilla JavaScript
- **Design**: Dark mode, gold/amber accents, glassmorphism, responsive layout

## 📦 Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### 3. Set Up API Keys
Edit `.env` file:
```env
GEMINI_API_KEY=your-key    # Free at https://aistudio.google.com/apikey
GROQ_API_KEY=your-key      # Free at https://console.groq.com
```

### 4. Run the Application
```bash
python app.py
```

### 5. Open Browser
```
http://localhost:5000
```

## 📂 Project Structure

```
Legal-sum/
├── app.py                  # Flask main app with all routes
├── ai_analyzer.py          # Multi-provider LLM (Gemini/Groq)
├── legal_chatbot.py        # Conversational AI chatbot
├── document_drafter.py     # Legal document generation
├── legal_ner.py            # spaCy-based Named Entity Recognition
├── ipc_lookup.py           # IPC/BNS section database
├── nlp_model.py            # TF-IDF case matching model
├── summarizer.py           # Hybrid extractive + abstractive summarizer
├── pdf_extractor.py        # PDF text extraction
├── database.py             # SQLite persistence layer
├── requirements.txt        # Python dependencies
├── .env                    # API keys configuration
├── templates/
│   ├── landing.html        # Landing page
│   ├── dashboard.html      # Dashboard with sidebar
│   ├── index.html          # Case search page
│   ├── chatbot.html        # AI chatbot interface
│   ├── drafter.html        # Document drafter
│   └── ipc_lookup.html     # IPC/BNS lookup
├── static/
│   ├── modern.css          # Dark legal-themed stylesheet
│   └── script.js           # Search page JavaScript
└── Dataset/                # 400+ legal case PDFs
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/search` | Search similar cases |
| POST | `/api/chat` | Chat with legal AI |
| POST | `/api/draft` | Draft legal documents |
| GET | `/api/ipc-lookup?q=` | Search IPC sections |
| POST | `/api/ipc-suggest` | Suggest sections from case |
| POST | `/api/ner` | Extract legal entities |
| POST | `/api/summarize` | Summarize legal text |
| GET | `/api/stats` | Get usage statistics |
| GET | `/api/history` | Get search history |

## 📊 NLP Pipeline

1. **PDF Extraction** → PyPDF2 extracts text from 400+ legal case documents
2. **Text Vectorization** → TF-IDF (unigrams + bigrams, 5000 features)
3. **Case Matching** → Cosine similarity between query and case vectors
4. **Summarization** → Extractive (sentence scoring with legal keyword boosting) + LLM abstractive
5. **Entity Recognition** → spaCy with custom EntityRuler for legal entities
6. **AI Analysis** → Google Gemini generates structured JSON analysis with verdict prediction

## ⚠ Notes

- First run extracts text from PDFs and caches to `extracted_data.pkl`
- Without API keys, NLP features (search, NER, summarization) still work
- AI features (chatbot, verdict prediction, drafter) require Gemini or Groq API key
- Both Gemini and Groq offer free tiers sufficient for development/demo
