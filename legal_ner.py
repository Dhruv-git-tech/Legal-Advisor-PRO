import re
import json

class LegalNER:
    """Named Entity Recognition for legal documents using spaCy + custom rules"""
    
    def __init__(self):
        self.nlp = None
        self._initialized = False
        self._init_error = None
        self._initialize()
    
    def _initialize(self):
        """Initialize spaCy with custom legal entity patterns"""
        try:
            import spacy
            from spacy.language import Language
            
            # Load English model
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("⚠ spaCy model not found. Run: python -m spacy download en_core_web_sm")
                self._init_error = "spaCy model 'en_core_web_sm' not installed"
                return
            
            # Add custom legal entity patterns using EntityRuler
            if "entity_ruler" not in self.nlp.pipe_names:
                ruler = self.nlp.add_pipe("entity_ruler", before="ner")
            else:
                ruler = self.nlp.get_pipe("entity_ruler")
            
            patterns = self._get_legal_patterns()
            ruler.add_patterns(patterns)
            
            self._initialized = True
            print("✓ Legal NER initialized with spaCy + custom patterns")
            
        except ImportError:
            self._init_error = "spaCy not installed. Run: pip install spacy"
            print(f"⚠ {self._init_error}")
        except Exception as e:
            self._init_error = str(e)
            print(f"⚠ NER initialization error: {e}")
    
    def _get_legal_patterns(self):
        """Get custom entity patterns for legal domain"""
        patterns = []
        
        # Court names
        courts = [
            "Supreme Court", "High Court", "District Court", "Sessions Court",
            "Magistrate Court", "Family Court", "Consumer Court", "Tribunal",
            "Supreme Court of India", "National Consumer Disputes Redressal Commission",
            "NCDRC", "NCLT", "National Company Law Tribunal", "ITAT",
            "Delhi High Court", "Bombay High Court", "Madras High Court",
            "Calcutta High Court", "Allahabad High Court", "Karnataka High Court"
        ]
        for court in courts:
            patterns.append({"label": "COURT", "pattern": court})
        
        # Legal acts
        acts = [
            "Indian Penal Code", "IPC", "Code of Criminal Procedure", "CrPC",
            "Code of Civil Procedure", "CPC", "Indian Evidence Act",
            "Constitution of India", "Motor Vehicles Act", "NDPS Act",
            "Information Technology Act", "Consumer Protection Act",
            "Hindu Marriage Act", "Indian Contract Act", "Transfer of Property Act",
            "Negotiable Instruments Act", "Companies Act", "Arbitration Act",
            "POCSO Act", "Domestic Violence Act", "Right to Information Act",
            "Bharatiya Nyaya Sanhita", "BNS", "Bharatiya Nagarik Suraksha Sanhita",
            "BNSS", "Bharatiya Sakshya Adhiniyam", "BSA"
        ]
        for act in acts:
            patterns.append({"label": "LAW", "pattern": act})
        
        # Section references using token patterns
        patterns.append({
            "label": "SECTION",
            "pattern": [
                {"LOWER": "section"},
                {"IS_DIGIT": True}
            ]
        })
        patterns.append({
            "label": "SECTION", 
            "pattern": [
                {"LOWER": "sec"},
                {"IS_PUNCT": True, "OP": "?"},
                {"IS_DIGIT": True}
            ]
        })
        patterns.append({
            "label": "SECTION",
            "pattern": [
                {"LOWER": {"IN": ["u/s", "u/sec"]}}
            ]
        })
        
        # Legal roles
        roles = [
            "petitioner", "respondent", "plaintiff", "defendant",
            "appellant", "complainant", "accused", "witness",
            "advocate", "judge", "magistrate", "prosecutor"
        ]
        for role in roles:
            patterns.append({"label": "LEGAL_ROLE", "pattern": [{"LOWER": role}]})
        
        return patterns
    
    def extract_entities(self, text):
        """Extract named entities from legal text"""
        if not self._initialized:
            return self._fallback_extraction(text)
        
        # Process text with spaCy
        doc = self.nlp(text[:100000])  # Limit to 100k chars for performance
        
        entities = {
            "persons": [],
            "organizations": [],
            "courts": [],
            "laws": [],
            "sections": [],
            "dates": [],
            "locations": [],
            "legal_roles": [],
            "monetary": []
        }
        
        seen = set()
        
        for ent in doc.ents:
            key = (ent.label_, ent.text.strip())
            if key in seen or len(ent.text.strip()) < 2:
                continue
            seen.add(key)
            
            entity_data = {"text": ent.text.strip(), "label": ent.label_}
            
            if ent.label_ == "PERSON":
                entities["persons"].append(entity_data)
            elif ent.label_ == "ORG":
                entities["organizations"].append(entity_data)
            elif ent.label_ == "COURT":
                entities["courts"].append(entity_data)
            elif ent.label_ == "LAW":
                entities["laws"].append(entity_data)
            elif ent.label_ == "SECTION":
                entities["sections"].append(entity_data)
            elif ent.label_ == "DATE":
                entities["dates"].append(entity_data)
            elif ent.label_ in ("GPE", "LOC"):
                entities["locations"].append(entity_data)
            elif ent.label_ == "LEGAL_ROLE":
                entities["legal_roles"].append(entity_data)
            elif ent.label_ == "MONEY":
                entities["monetary"].append(entity_data)
        
        # Also extract sections via regex (more reliable)
        section_matches = re.findall(
            r'(?:Section|Sec\.?|S\.?|U/[Ss])\s*(\d+[A-Za-z]*)',
            text
        )
        for sec in section_matches:
            entry = {"text": f"Section {sec}", "label": "SECTION"}
            if entry not in entities["sections"]:
                entities["sections"].append(entry)
        
        # Limit each category to top 15
        for key in entities:
            entities[key] = entities[key][:15]
        
        return {
            "success": True,
            "entities": entities,
            "total_entities": sum(len(v) for v in entities.values())
        }
    
    def _fallback_extraction(self, text):
        """Regex-based fallback when spaCy is not available"""
        entities = {
            "persons": [],
            "organizations": [],
            "courts": [],
            "laws": [],
            "sections": [],
            "dates": [],
            "locations": [],
            "legal_roles": [],
            "monetary": []
        }
        
        # Extract sections
        sections = re.findall(r'(?:Section|Sec\.?)\s*(\d+[A-Za-z]*)', text, re.IGNORECASE)
        for sec in set(sections):
            entities["sections"].append({"text": f"Section {sec}", "label": "SECTION"})
        
        # Extract court names
        court_patterns = re.findall(
            r'(?:Supreme Court|High Court|District Court|Sessions Court|Magistrate Court|Tribunal)',
            text, re.IGNORECASE
        )
        for court in set(court_patterns):
            entities["courts"].append({"text": court, "label": "COURT"})
        
        # Extract acts
        act_patterns = re.findall(
            r'(?:Indian Penal Code|IPC|CrPC|CPC|Evidence Act|Constitution|BNS|BNSS)',
            text, re.IGNORECASE
        )
        for act in set(act_patterns):
            entities["laws"].append({"text": act, "label": "LAW"})
        
        # Extract dates
        date_patterns = re.findall(
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4}',
            text, re.IGNORECASE
        )
        for date in set(date_patterns):
            entities["dates"].append({"text": date, "label": "DATE"})
        
        # Extract monetary amounts
        money_patterns = re.findall(
            r'(?:Rs\.?|INR|₹)\s*[\d,]+(?:\.\d{2})?(?:\s*(?:lakh|crore|thousand))?',
            text, re.IGNORECASE
        )
        for money in set(money_patterns):
            entities["monetary"].append({"text": money, "label": "MONEY"})
        
        return {
            "success": True,
            "entities": entities,
            "total_entities": sum(len(v) for v in entities.values()),
            "note": self._init_error or "Using regex fallback (spaCy not available)"
        }
    
    def is_available(self):
        """Check if NER is initialized"""
        return self._initialized
