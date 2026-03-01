import os
import json
import time

class LegalAIAnalyzer:
    """AI-powered legal case analyzer using Google Gemini (primary) and Groq (fallback)"""
    
    def __init__(self):
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.groq_key = os.getenv('GROQ_API_KEY')
        self.gemini_model = "gemini-2.0-flash"
        self.groq_model = "llama-3.3-70b-versatile"
        self.enabled = bool(self.gemini_key or self.groq_key)
        self._active_provider = None
    
    def _call_gemini(self, prompt, system_prompt="You are a legal expert specializing in Indian law."):
        """Call Google Gemini API using the new google.genai SDK"""
        from google import genai
        client = genai.Client(api_key=self.gemini_key)
        response = client.models.generate_content(
            model=self.gemini_model,
            contents=prompt,
            config={
                "system_instruction": system_prompt,
                "temperature": 0.3,
                "max_output_tokens": 2000,
            }
        )
        self._active_provider = "Gemini"
        return response.text
    
    def _call_groq(self, prompt, system_prompt="You are a legal expert specializing in Indian law."):
        """Call Groq API as fallback"""
        from groq import Groq
        client = Groq(api_key=self.groq_key)
        response = client.chat.completions.create(
            model=self.groq_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000,
        )
        self._active_provider = "Groq"
        return response.choices[0].message.content
    
    def call_llm(self, prompt, system_prompt="You are a legal expert specializing in Indian law."):
        """Call LLM with automatic fallback: Gemini → Groq"""
        errors = []
        
        # Try Gemini first
        if self.gemini_key:
            try:
                return self._call_gemini(prompt, system_prompt)
            except Exception as e:
                errors.append(f"Gemini: {str(e)}")
                print(f"⚠ Gemini failed: {e}")
        
        # Fallback to Groq
        if self.groq_key:
            try:
                return self._call_groq(prompt, system_prompt)
            except Exception as e:
                errors.append(f"Groq: {str(e)}")
                print(f"⚠ Groq failed: {e}")
        
        raise Exception(f"All LLM providers failed: {'; '.join(errors)}")
    
    def analyze_case(self, case_study, matched_cases):
        """Analyze case and provide verdict prediction using AI"""
        if not self.enabled:
            return {
                'available': False,
                'error': 'No API keys configured. Set GEMINI_API_KEY or GROQ_API_KEY.'
            }
        
        try:
            top_case = matched_cases[0] if matched_cases else None
            if not top_case:
                return {'available': False, 'error': 'No matched cases found for analysis'}
            
            prompt = self._create_analysis_prompt(case_study, top_case, matched_cases[:3])
            raw_response = self.call_llm(prompt)
            analysis = self._parse_json_response(raw_response)
            
            return {
                'available': True,
                'analysis': analysis,
                'top_case_name': top_case.get('case_name', 'Unknown'),
                'provider': self._active_provider
            }
        except Exception as e:
            return {'available': False, 'error': f'Error in AI analysis: {str(e)}'}
    
    def _create_analysis_prompt(self, case_study, top_case, matched_cases):
        """Create a comprehensive prompt for case analysis"""
        matched_cases_text = ""
        for idx, case in enumerate(matched_cases, 1):
            matched_cases_text += f"\n{idx}. Case: {case.get('case_name', 'Unknown')}\n"
            matched_cases_text += f"   Similarity: {case.get('similarity_score', 0)}%\n"
        
        prompt = f"""You are a senior legal analyst with expertise in Indian law. Analyze the following case and provide a comprehensive assessment.

**CURRENT CASE TO ANALYZE:**
{case_study}

**TOP SIMILAR REFERENCE CASES FROM LEGAL DATABASE:**
{matched_cases_text}

**TASK:**
1. Analyze the legal issues in the current case
2. Identify key legal principles applicable
3. Examine the similarity to the reference cases provided
4. Assess the strength of the plaintiff's case
5. Predict the likely verdict with reasoning
6. Provide percentage probability of winning for each party

**OUTPUT FORMAT (JSON):**
{{
    "legal_issues": ["List of main legal issues"],
    "applicable_laws": ["List of relevant laws and acts"],
    "key_facts": ["Most important factual points"],
    "plaintiff_strengths": ["Advantages for plaintiff"],
    "plaintiff_weaknesses": ["Disadvantages for plaintiff"],
    "defendant_strengths": ["Advantages for defendant"],
    "defendant_weaknesses": ["Disadvantages for defendant"],
    "similarity_to_reference_cases": "How similar is this to the reference cases",
    "precedent_value": "How helpful are the reference cases",
    "verdict_prediction": "win or loss or draw",
    "confidence_level": "high/medium/low",
    "win_probability_plaintiff": 0-100,
    "win_probability_defendant": 0-100,
    "reasoning": "Detailed explanation of the analysis",
    "recommended_legal_strategy": "Strategic advice for the case"
}}

Provide your analysis in valid JSON format only. No markdown formatting."""
        return prompt
    
    def _parse_json_response(self, content):
        """Parse JSON from LLM response, handling markdown wrappers"""
        try:
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            return json.loads(content)
        except:
            return {"raw_analysis": content}
    
    def is_available(self):
        """Check if AI analyzer is available"""
        return self.enabled
    
    def get_provider_info(self):
        """Return info about available providers"""
        providers = []
        if self.gemini_key:
            providers.append("Google Gemini (gemini-2.0-flash)")
        if self.groq_key:
            providers.append("Groq (Llama 3.3 70B)")
        return providers
