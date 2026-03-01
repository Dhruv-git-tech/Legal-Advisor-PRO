import os
import json
from ai_analyzer import LegalAIAnalyzer

class LegalChatbot:
    """Conversational AI chatbot for legal queries using Gemini/Groq"""
    
    SYSTEM_PROMPT = """You are LegalAI Assistant, an expert AI legal advisor specializing in Indian law. You help users understand:
- Indian Penal Code (IPC) and Bharatiya Nyaya Sanhita (BNS) sections
- Criminal and civil procedures (CrPC, CPC)
- Constitutional rights and fundamental rights
- Property law, family law, labor law, cyber law
- Legal procedures: filing FIR, bail, appeals
- Consumer protection, RTI, POCSO

Guidelines:
- Always provide accurate, helpful legal information
- Cite specific sections, acts, and precedents when relevant
- Use simple language accessible to non-lawyers
- Add disclaimers that this is AI guidance, not professional legal advice
- If unsure, clearly state limitations
- Format responses with bullet points and clear structure
- Be empathetic and supportive in tone"""

    def __init__(self):
        self.analyzer = LegalAIAnalyzer()
        self.conversations = {}
    
    def chat(self, session_id, user_message):
        """Process a chat message and return AI response"""
        if not self.analyzer.is_available():
            return {
                'success': False,
                'error': 'No AI provider configured. Please set GEMINI_API_KEY or GROQ_API_KEY.'
            }
        
        # Get or create conversation history
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        history = self.conversations[session_id]
        history.append({"role": "user", "content": user_message})
        
        # Build context from history (keep last 10 messages)
        context_messages = history[-10:]
        conversation_context = "\n".join(
            f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
            for m in context_messages[:-1]
        )
        
        prompt = f"""Previous conversation:
{conversation_context}

Current user question: {user_message}

Provide a helpful, accurate legal response. Use bullet points and clear formatting. Be concise but thorough."""
        
        try:
            response = self.analyzer.call_llm(prompt, self.SYSTEM_PROMPT)
            
            # Store response in history
            history.append({"role": "assistant", "content": response})
            
            # Keep history manageable
            if len(history) > 20:
                history = history[-20:]
                self.conversations[session_id] = history
            
            return {
                'success': True,
                'response': response,
                'provider': self.analyzer._active_provider
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to get AI response: {str(e)}'
            }
    
    def get_suggested_prompts(self):
        """Return suggested legal questions for the user"""
        return [
            "What are my rights if I am arrested?",
            "How do I file an FIR at a police station?",
            "Explain Section 302 of IPC in simple terms",
            "What is the process for getting bail?",
            "What are grounds for divorce under Hindu Marriage Act?",
            "How to file a consumer complaint online?",
            "What is the difference between IPC and BNS?",
            "Explain fundamental rights under Indian Constitution",
            "What is anticipatory bail and how to apply?",
            "What are the penalties for cybercrime in India?"
        ]
    
    def clear_history(self, session_id):
        """Clear conversation history for a session"""
        if session_id in self.conversations:
            del self.conversations[session_id]
        return {'success': True, 'message': 'Chat history cleared'}
