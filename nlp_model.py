from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class LegalCaseMatcher:
    """Simple TF-IDF based model for finding similar legal cases"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)  # Use unigrams and bigrams
        )
        self.case_vectors = None
        self.case_names = None
    
    def train(self, texts, filenames):
        """
        Train the model on case texts
        
        Args:
            texts: List of case texts
            filenames: List of case filenames
        """
        print("Vectorizing cases...")
        self.case_vectors = self.vectorizer.fit_transform(texts)
        self.case_names = filenames
        print("Training complete!")
    
    def find_similar_cases(self, query_text, top_n=5):
        """
        Find similar cases based on query text
        
        Args:
            query_text: Case study input text
            top_n: Number of similar cases to return
            
        Returns:
            List of dictionaries with case names and similarity scores
        """
        if self.case_vectors is None:
            raise ValueError("Model not trained yet!")
        
        # Transform query text to vector
        query_vector = self.vectorizer.transform([query_text])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.case_vectors).flatten()
        
        # Get top N most similar cases
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        results = []
        for idx in top_indices:
            similarity = float(similarities[idx])
            case_name = self.format_case_name(self.case_names[idx])
            results.append({
                'case_name': case_name,
                'similarity_score': round(similarity * 100, 2),  # Convert to percentage
                'filename': self.case_names[idx]
            })
        
        return results
    
    def format_case_name(self, filename):
        """Format filename to readable case name"""
        # Remove .PDF extension
        name = filename.replace('_1.PDF', '').replace('.PDF', '')
        # Replace underscores with spaces
        name = name.replace('_', ' ')
        # Split into title case words
        words = name.split()
        formatted = ' '.join(word.capitalize() for word in words)
        return formatted

