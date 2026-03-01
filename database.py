import sqlite3
import json
import os
from datetime import datetime

class Database:
    """SQLite database for persistent storage of search history, chat history, and drafted documents"""
    
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'legal_assistant.db')
    
    def __init__(self):
        self._create_tables()
    
    def _get_conn(self):
        """Get a database connection"""
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                summarized_query TEXT,
                results TEXT,
                ai_analysis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                provider TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drafted_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_type TEXT NOT NULL,
                details TEXT,
                document TEXT NOT NULL,
                provider TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✓ Database initialized.")
    
    # Search History
    def save_search(self, query, summarized_query, results, ai_analysis):
        """Save a search query and results"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO search_history (query, summarized_query, results, ai_analysis) VALUES (?, ?, ?, ?)',
            (query, summarized_query, json.dumps(results), json.dumps(ai_analysis))
        )
        conn.commit()
        conn.close()
    
    def get_search_history(self, limit=20):
        """Get recent search history"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM search_history ORDER BY created_at DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # Chat History
    def save_chat_message(self, session_id, role, message, provider=None):
        """Save a chat message"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO chat_history (session_id, role, message, provider) VALUES (?, ?, ?, ?)',
            (session_id, role, message, provider)
        )
        conn.commit()
        conn.close()
    
    def get_chat_history(self, session_id, limit=50):
        """Get chat history for a session"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM chat_history WHERE session_id = ? ORDER BY created_at ASC LIMIT ?',
            (session_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # Drafted Documents
    def save_document(self, doc_type, details, document, provider=None):
        """Save a drafted document"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO drafted_documents (doc_type, details, document, provider) VALUES (?, ?, ?, ?)',
            (doc_type, json.dumps(details), document, provider)
        )
        conn.commit()
        conn.close()
    
    def get_document_history(self, limit=20):
        """Get recent drafted documents"""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM drafted_documents ORDER BY created_at DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # Stats
    def get_stats(self):
        """Get usage statistics"""
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM search_history')
        searches = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM chat_history WHERE role = "user"')
        chats = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM drafted_documents')
        docs = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            'total_searches': searches,
            'total_chats': chats,
            'total_documents': docs
        }
