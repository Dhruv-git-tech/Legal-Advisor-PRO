import re
from collections import Counter

class LegalCaseSummarizer:
    """Hybrid summarizer: fast extractive + LLM-based abstractive for legal cases"""
    
    def __init__(self):
        self.stop_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
            'this', 'said', 'each', 'which', 'their', 'time', 'if', 'will',
            'about', 'how', 'up', 'out', 'many', 'then', 'them', 'these', 'can',
            'him', 'has', 'been', 'when', 'than', 'its', 'who', 'oil', 'sit',
            'now', 'find', 'down', 'day', 'did', 'get', 'made', 'may',
            'also', 'upon', 'said', 'against'
        }
        self._analyzer = None
    
    def _get_analyzer(self):
        """Lazy-load AI analyzer for abstractive summarization"""
        if self._analyzer is None:
            try:
                from ai_analyzer import LegalAIAnalyzer
                self._analyzer = LegalAIAnalyzer()
            except:
                pass
        return self._analyzer
    
    def summarize(self, text, max_sentences=3, use_llm=False):
        """
        Summarize text using extractive method, or LLM for better quality
        
        Args:
            text: Input text to summarize
            max_sentences: Max sentences in extractive summary
            use_llm: Whether to use LLM for abstractive summarization
        """
        if not text or len(text.strip()) < 50:
            return text
        
        if use_llm:
            llm_summary = self._abstractive_summarize(text)
            if llm_summary:
                return llm_summary
        
        return self._extractive_summarize(text, max_sentences)
    
    def _abstractive_summarize(self, text):
        """Use LLM for high-quality abstractive summarization"""
        analyzer = self._get_analyzer()
        if not analyzer or not analyzer.is_available():
            return None
        
        try:
            prompt = f"""Summarize the following legal case text in 3-5 concise sentences. Focus on:
1. The main legal issue or dispute
2. Key parties involved
3. The court's decision or current status
4. Applicable laws or sections

Text to summarize:
{text[:5000]}

Provide a clear, concise summary:"""
            
            return analyzer.call_llm(
                prompt,
                "You are a legal document summarizer. Provide concise, accurate summaries."
            )
        except:
            return None
    
    def _extractive_summarize(self, text, max_sentences=3):
        """Fast extractive summarization using sentence scoring"""
        sentences = self._split_into_sentences(text)
        
        if len(sentences) <= max_sentences:
            return text
        
        sentence_scores = self._calculate_scores(sentences)
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:max_sentences]
        top_sentences = sorted(top_sentences, key=lambda x: sentences.index(x[0]))
        summary = ' '.join([sent for sent, _ in top_sentences])
        
        return summary
    
    def summarize_case_study(self, case_text, max_sentences=3):
        """Summarize a case study text for better analysis"""
        return self.summarize(case_text, max_sentences)
    
    def _split_into_sentences(self, text):
        """Split text into sentences"""
        text = re.sub(r'\s+', ' ', text)
        sentences = re.split(r'[.!?]\s+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        return sentences
    
    def _calculate_scores(self, sentences):
        """Calculate importance scores for each sentence"""
        scores = {}
        word_freq = self._word_frequency(sentences)
        
        legal_keywords = [
            'court', 'case', 'judgment', 'petitioner', 'respondent',
            'plaintiff', 'defendant', 'order', 'appeal', 'evidence',
            'witness', 'law', 'act', 'section', 'statute', 'contract',
            'agreement', 'property', 'rights', 'claims', 'damages',
            'verdict', 'conviction', 'acquittal', 'bail', 'sentence',
            'prosecution', 'defense', 'tribunal', 'constitution',
            'fundamental', 'article', 'amendment', 'provision'
        ]
        
        for sentence in sentences:
            score = 0
            words = self._extract_words(sentence)
            
            for word in words:
                if word in word_freq:
                    score += word_freq[word]
            
            if len(words) > 0:
                scores[sentence] = score / len(words)
            else:
                scores[sentence] = 0
            
            keyword_count = sum(1 for word in words if word.lower() in legal_keywords)
            if keyword_count > 0:
                scores[sentence] += keyword_count * 0.15
            
            # Boost first and second sentences (often contain key info)
            idx = sentences.index(sentence)
            if idx == 0:
                scores[sentence] *= 1.3
            elif idx == 1:
                scores[sentence] *= 1.15
        
        return scores
    
    def _extract_words(self, text):
        """Extract words from text"""
        words = re.findall(r'\b\w+\b', text.lower())
        words = [w for w in words if w not in self.stop_words and len(w) > 2]
        return words
    
    def _word_frequency(self, sentences):
        """Calculate word frequency across all sentences"""
        word_freq = Counter()
        for sentence in sentences:
            words = self._extract_words(sentence)
            word_freq.update(words)
        
        if word_freq:
            max_freq = max(word_freq.values())
            word_freq = {word: freq / max_freq for word, freq in word_freq.items()}
        
        return word_freq
