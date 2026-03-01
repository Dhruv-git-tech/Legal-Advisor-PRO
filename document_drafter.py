import os
import json
from ai_analyzer import LegalAIAnalyzer

class DocumentDrafter:
    """AI-powered legal document drafting using Gemini/Groq"""
    
    DOCUMENT_TYPES = {
        "fir": {
            "name": "First Information Report (FIR)",
            "description": "Draft an FIR to be filed at a police station",
            "fields": ["complainant_name", "date_of_incident", "place_of_incident", "description_of_incident", "accused_details", "witnesses"]
        },
        "legal_notice": {
            "name": "Legal Notice",
            "description": "Draft a formal legal notice to be sent to the opposing party",
            "fields": ["sender_name", "sender_address", "recipient_name", "recipient_address", "subject", "facts", "demand", "timeline"]
        },
        "complaint": {
            "name": "Consumer/Civil Complaint",
            "description": "Draft a complaint for consumer forum or civil court",
            "fields": ["complainant_name", "respondent_name", "nature_of_complaint", "facts", "relief_sought", "supporting_documents"]
        },
        "bail_application": {
            "name": "Bail Application",
            "description": "Draft a bail application for court submission",
            "fields": ["applicant_name", "case_number", "charges", "grounds_for_bail", "surety_details", "court_name"]
        },
        "affidavit": {
            "name": "Affidavit",
            "description": "Draft a sworn statement / affidavit",
            "fields": ["deponent_name", "deponent_address", "purpose", "facts_to_state", "court_or_authority"]
        },
        "rti_application": {
            "name": "RTI Application",
            "description": "Draft a Right to Information application",
            "fields": ["applicant_name", "applicant_address", "public_authority", "information_required", "period_of_information"]
        }
    }
    
    def __init__(self):
        self.analyzer = LegalAIAnalyzer()
    
    def get_document_types(self):
        """Return available document types with their fields"""
        return {
            doc_type: {
                "name": info["name"],
                "description": info["description"],
                "fields": info["fields"]
            }
            for doc_type, info in self.DOCUMENT_TYPES.items()
        }
    
    def draft_document(self, doc_type, details):
        """Generate a legal document based on type and provided details"""
        if not self.analyzer.is_available():
            return {
                'success': False,
                'error': 'No AI provider configured. Please set GEMINI_API_KEY or GROQ_API_KEY.'
            }
        
        if doc_type not in self.DOCUMENT_TYPES:
            return {
                'success': False,
                'error': f'Unknown document type: {doc_type}. Available: {", ".join(self.DOCUMENT_TYPES.keys())}'
            }
        
        doc_info = self.DOCUMENT_TYPES[doc_type]
        
        prompt = self._create_draft_prompt(doc_type, doc_info, details)
        
        system_prompt = """You are a professional Indian legal document drafter. You create legally accurate, properly formatted documents following Indian legal standards. Include proper formatting with:
- Proper headers and case details
- Legal terminology and formal language
- Relevant sections of applicable laws
- Proper signature blocks and verification
- Date and place fields
Format the document professionally. Use proper spacing and structure."""
        
        try:
            response = self.analyzer.call_llm(prompt, system_prompt)
            
            return {
                'success': True,
                'document': response,
                'document_type': doc_info['name'],
                'provider': self.analyzer._active_provider
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to draft document: {str(e)}'
            }
    
    def _create_draft_prompt(self, doc_type, doc_info, details):
        """Create a prompt for document drafting"""
        details_text = "\n".join(f"- {key.replace('_', ' ').title()}: {value}" for key, value in details.items() if value)
        
        prompt = f"""Draft a professional {doc_info['name']} with the following details:

{details_text}

Requirements:
1. Follow standard Indian legal format for {doc_info['name']}
2. Use proper legal language and terminology
3. Include all necessary sections and clauses
4. Reference applicable Indian laws and sections
5. Include proper date, place, and signature blocks
6. Make it comprehensive and legally sound

Generate the complete document text ready for use."""
        
        return prompt
