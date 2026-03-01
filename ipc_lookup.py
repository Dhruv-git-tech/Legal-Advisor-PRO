import json

class IPCLookup:
    """Indian Penal Code / Bharatiya Nyaya Sanhita section lookup with AI explanations"""
    
    def __init__(self):
        self.sections = self._load_sections()
    
    def _load_sections(self):
        """Load IPC/BNS section database"""
        return {
            # Offences Against the Body
            "299": {"title": "Culpable Homicide", "category": "Offences Against Body", "punishment": "Imprisonment up to 10 years + fine", "bns": "Section 100", "description": "Whoever causes death by doing an act with the intention of causing death, or with the knowledge that it is likely to cause death."},
            "300": {"title": "Murder", "category": "Offences Against Body", "punishment": "Death or life imprisonment + fine", "bns": "Section 101", "description": "Culpable homicide is murder if the act is done with the intention of causing death, or bodily injury sufficient to cause death."},
            "302": {"title": "Punishment for Murder", "category": "Offences Against Body", "punishment": "Death or life imprisonment + fine", "bns": "Section 103", "description": "Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine."},
            "304": {"title": "Culpable Homicide not amounting to Murder", "category": "Offences Against Body", "punishment": "Life imprisonment or imprisonment up to 10 years + fine", "bns": "Section 105", "description": "If the act is done with knowledge that it is likely to cause death but without intention."},
            "304A": {"title": "Death by Negligence", "category": "Offences Against Body", "punishment": "Imprisonment up to 2 years + fine", "bns": "Section 106", "description": "Causing death by rash or negligent act not amounting to culpable homicide."},
            "307": {"title": "Attempt to Murder", "category": "Offences Against Body", "punishment": "Imprisonment up to 10 years + fine; life imprisonment if hurt caused", "bns": "Section 109", "description": "Whoever does any act with intention or knowledge to cause death."},
            "319": {"title": "Hurt", "category": "Offences Against Body", "punishment": "Imprisonment up to 1 year + fine up to Rs 1000", "bns": "Section 114", "description": "Whoever causes bodily pain, disease or infirmity to any person."},
            "320": {"title": "Grievous Hurt", "category": "Offences Against Body", "punishment": "Imprisonment up to 7 years + fine", "bns": "Section 115", "description": "Emasculation, permanent privation of sight/hearing, fracture, etc."},
            "323": {"title": "Voluntarily Causing Hurt", "category": "Offences Against Body", "punishment": "Imprisonment up to 1 year or fine up to Rs 1000 or both", "bns": "Section 118", "description": "Whoever voluntarily causes hurt shall be punished."},
            "326": {"title": "Voluntarily Causing Grievous Hurt by Dangerous Weapons", "category": "Offences Against Body", "punishment": "Life imprisonment or imprisonment up to 10 years + fine", "bns": "Section 122", "description": "Causing grievous hurt by means of any instrument for shooting, stabbing or cutting."},
            
            # Theft & Property
            "378": {"title": "Theft", "category": "Property Offences", "punishment": "Imprisonment up to 3 years or fine or both", "bns": "Section 303", "description": "Whoever intending to take dishonestly any moveable property out of possession of any person without consent."},
            "379": {"title": "Punishment for Theft", "category": "Property Offences", "punishment": "Imprisonment up to 3 years or fine or both", "bns": "Section 305", "description": "Whoever commits theft shall be punished with imprisonment or fine or both."},
            "380": {"title": "Theft in Dwelling House", "category": "Property Offences", "punishment": "Imprisonment up to 7 years + fine", "bns": "Section 306", "description": "Whoever commits theft in any building used as human dwelling or custody of property."},
            "383": {"title": "Extortion", "category": "Property Offences", "punishment": "Imprisonment up to 3 years or fine or both", "bns": "Section 308", "description": "Whoever intentionally puts any person in fear of injury including to reputation."},
            "390": {"title": "Robbery", "category": "Property Offences", "punishment": "Rigorous imprisonment up to 10 years + fine", "bns": "Section 309", "description": "In all robbery there is either theft or extortion combined with violence."},
            "392": {"title": "Punishment for Robbery", "category": "Property Offences", "punishment": "Rigorous imprisonment up to 10 years + fine", "bns": "Section 309(2)", "description": "Whoever commits robbery shall be punished with rigorous imprisonment."},
            "395": {"title": "Dacoity", "category": "Property Offences", "punishment": "Life imprisonment or rigorous imprisonment up to 10 years + fine", "bns": "Section 310", "description": "When five or more persons conjointly commit or attempt robbery."},
            
            # Cheating & Fraud
            "406": {"title": "Criminal Breach of Trust", "category": "Cheating & Fraud", "punishment": "Imprisonment up to 3 years or fine or both", "bns": "Section 316", "description": "Whoever being entrusted with property dishonestly misappropriates or converts to his own use."},
            "415": {"title": "Cheating", "category": "Cheating & Fraud", "punishment": "Imprisonment up to 1 year or fine or both", "bns": "Section 318", "description": "Whoever by deceiving any person induces them to deliver property or consent."},
            "420": {"title": "Cheating and Dishonestly Inducing Delivery of Property", "category": "Cheating & Fraud", "punishment": "Imprisonment up to 7 years + fine", "bns": "Section 318(4)", "description": "Whoever cheats and thereby dishonestly induces the person to deliver property."},
            "463": {"title": "Forgery", "category": "Cheating & Fraud", "punishment": "Imprisonment up to 2 years or fine or both", "bns": "Section 336", "description": "Making a false document with intent to cause damage or injury."},
            "468": {"title": "Forgery for Purpose of Cheating", "category": "Cheating & Fraud", "punishment": "Imprisonment up to 7 years + fine", "bns": "Section 338", "description": "Whoever commits forgery intending that the document shall be used for cheating."},
            
            # Sexual Offences
            "354": {"title": "Assault on Woman with Intent to Outrage her Modesty", "category": "Sexual Offences", "punishment": "Imprisonment 1-5 years + fine", "bns": "Section 74", "description": "Whoever assaults or uses criminal force on any woman intending to outrage her modesty."},
            "376": {"title": "Rape", "category": "Sexual Offences", "punishment": "Rigorous imprisonment 10 years to life + fine", "bns": "Section 63", "description": "Sexual intercourse against will, without consent, or with consent obtained under fear or intoxication."},
            "498A": {"title": "Cruelty by Husband or Relatives", "category": "Matrimonial Offences", "punishment": "Imprisonment up to 3 years + fine", "bns": "Section 84", "description": "Husband or relative subjecting woman to cruelty (including dowry demands)."},
            "304B": {"title": "Dowry Death", "category": "Matrimonial Offences", "punishment": "Imprisonment 7 years to life", "bns": "Section 80", "description": "Death of woman within 7 years of marriage caused by burns/injury under abnormal circumstances."},
            
            # Defamation & Public Order
            "499": {"title": "Defamation", "category": "Defamation", "punishment": "Simple imprisonment up to 2 years or fine or both", "bns": "Section 356", "description": "Making or publishing imputation concerning any person intending to harm reputation."},
            "500": {"title": "Punishment for Defamation", "category": "Defamation", "punishment": "Simple imprisonment up to 2 years or fine or both", "bns": "Section 356", "description": "Whoever defames another shall be punished."},
            "506": {"title": "Criminal Intimidation", "category": "Criminal Intimidation", "punishment": "Imprisonment up to 2 years or fine or both", "bns": "Section 351", "description": "Whoever threatens another with injury to person, reputation or property."},
            "509": {"title": "Word, Gesture or Act to Insult Modesty of Woman", "category": "Sexual Offences", "punishment": "Simple imprisonment up to 3 years + fine", "bns": "Section 79", "description": "Whoever intending to insult the modesty of any woman."},
            
            # Kidnapping & Abduction
            "359": {"title": "Kidnapping", "category": "Kidnapping", "punishment": "Imprisonment up to 7 years + fine", "bns": "Section 137", "description": "Kidnapping from India or kidnapping from lawful guardianship."},
            "363": {"title": "Punishment for Kidnapping", "category": "Kidnapping", "punishment": "Imprisonment up to 7 years + fine", "bns": "Section 137(2)", "description": "Whoever kidnaps any person from India or lawful guardianship."},
            "364": {"title": "Kidnapping for Ransom", "category": "Kidnapping", "punishment": "Death or life imprisonment", "bns": "Section 140", "description": "Whoever kidnaps or abducts any person in order to secretly and wrongfully confine."},
            
            # Cyber Crime
            "66": {"title": "Computer Related Offences (IT Act)", "category": "Cyber Crime", "punishment": "Imprisonment up to 3 years or fine up to 5 lakh", "bns": "IT Act Section 66", "description": "Dishonestly or fraudulently committing any act using computer resource."},
            "66A": {"title": "Sending Offensive Messages (IT Act - Struck Down)", "category": "Cyber Crime", "punishment": "Was: Imprisonment up to 3 years + fine (Struck down by SC in 2015)", "bns": "N/A", "description": "Sending grossly offensive or menacing messages. Note: Struck down by Supreme Court in Shreya Singhal v. Union of India."},
            "66B": {"title": "Receiving Stolen Computer Resource (IT Act)", "category": "Cyber Crime", "punishment": "Imprisonment up to 3 years or fine up to 1 lakh", "bns": "IT Act Section 66B", "description": "Dishonestly receiving or retaining any stolen computer resource."},
            "67": {"title": "Publishing Obscene Material Electronically (IT Act)", "category": "Cyber Crime", "punishment": "Imprisonment up to 5 years + fine up to 10 lakh", "bns": "IT Act Section 67", "description": "Publishing or transmitting obscene material in electronic form."},
            
            # Miscellaneous Important
            "34": {"title": "Common Intention", "category": "General Principles", "punishment": "N/A - Applied with other sections", "bns": "Section 3(5)", "description": "When a criminal act is done by several persons in furtherance of common intention, each person is liable as if done by himself alone."},
            "120B": {"title": "Criminal Conspiracy", "category": "General Principles", "punishment": "Same as the offence conspired for", "bns": "Section 61", "description": "When two or more persons agree to do an illegal act or legal act by illegal means."},
            "124A": {"title": "Sedition", "category": "Offences Against State", "punishment": "Life imprisonment or imprisonment up to 3 years + fine", "bns": "Section 150 (Revised)", "description": "Whoever brings or attempts to bring into hatred or contempt the Government established by law."},
            "153A": {"title": "Promoting Enmity Between Groups", "category": "Public Order", "punishment": "Imprisonment up to 3 years or fine or both", "bns": "Section 196", "description": "Promoting enmity between different groups on grounds of religion, race, language."},
            "295A": {"title": "Outraging Religious Feelings", "category": "Religious Offences", "punishment": "Imprisonment up to 3 years or fine or both", "bns": "Section 299", "description": "Deliberate and malicious acts intended to outrage religious feelings."},
            "341": {"title": "Wrongful Restraint", "category": "Criminal Force", "punishment": "Simple imprisonment up to 1 month or fine up to Rs 500 or both", "bns": "Section 126", "description": "Whoever wrongfully restrains any person."},
            "342": {"title": "Wrongful Confinement", "category": "Criminal Force", "punishment": "Imprisonment up to 1 year or fine up to Rs 1000 or both", "bns": "Section 127", "description": "Whoever wrongfully confines any person."},
            "503": {"title": "Criminal Intimidation", "category": "Criminal Intimidation", "punishment": "Imprisonment up to 2 years or fine or both", "bns": "Section 351", "description": "Threatening injury to person, reputation or property."},
            "511": {"title": "Attempt to Commit Offences", "category": "General Principles", "punishment": "Half of the longest term for that offence", "bns": "Section 62", "description": "Whoever attempts to commit an offence punishable with imprisonment."},
        }
    
    def search(self, query):
        """Search IPC sections by number, title, or keyword"""
        query_lower = query.lower().strip()
        results = []
        
        # Direct section number lookup
        clean_num = query_lower.replace("section", "").replace("sec", "").replace("ipc", "").replace(".", "").strip()
        if clean_num in self.sections:
            sec = self.sections[clean_num]
            results.append({"section": clean_num, **sec})
        
        # Keyword search in title and description
        if not results or len(query_lower) > 3:
            for sec_num, sec_data in self.sections.items():
                if sec_num == clean_num:
                    continue
                searchable = f"{sec_data['title']} {sec_data['description']} {sec_data['category']}".lower()
                if query_lower in searchable or all(word in searchable for word in query_lower.split()):
                    results.append({"section": sec_num, **sec_data})
        
        return results[:10]
    
    def get_section(self, section_number):
        """Get details of a specific section"""
        section_number = str(section_number).strip()
        if section_number in self.sections:
            return {"section": section_number, **self.sections[section_number]}
        return None
    
    def get_all_categories(self):
        """Get all section categories"""
        categories = {}
        for sec_num, sec_data in self.sections.items():
            cat = sec_data["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({"section": sec_num, "title": sec_data["title"]})
        return categories
    
    def suggest_sections(self, case_description):
        """Suggest applicable IPC sections from a case description (keyword-based)"""
        keywords_map = {
            "murder": ["299", "300", "302"],
            "kill": ["299", "300", "302", "304A"],
            "death": ["299", "300", "302", "304", "304A", "304B"],
            "hurt": ["319", "320", "323", "326"],
            "assault": ["323", "326", "354"],
            "theft": ["378", "379", "380"],
            "steal": ["378", "379", "380"],
            "rob": ["390", "392"],
            "dacoit": ["395"],
            "cheat": ["415", "420"],
            "fraud": ["415", "420", "468"],
            "forg": ["463", "468"],
            "rape": ["376"],
            "sexual": ["354", "376", "509"],
            "molestation": ["354", "509"],
            "dowry": ["304B", "498A"],
            "cruelty": ["498A"],
            "kidnap": ["359", "363", "364"],
            "abduct": ["359", "363"],
            "defam": ["499", "500"],
            "threaten": ["503", "506"],
            "intimidat": ["503", "506"],
            "conspir": ["120B"],
            "cyber": ["66", "66B", "67"],
            "online": ["66", "66A", "67"],
            "computer": ["66", "66B"],
            "sedition": ["124A"],
            "religion": ["153A", "295A"],
            "modesty": ["354", "509"],
            "restrain": ["341", "342"],
            "confine": ["342"],
            "negligence": ["304A"],
            "accident": ["304A"],
            "property": ["378", "379", "383", "406"],
            "trust": ["406"],
            "extort": ["383"],
        }
        
        case_lower = case_description.lower()
        suggested = set()
        
        for keyword, sections in keywords_map.items():
            if keyword in case_lower:
                suggested.update(sections)
        
        results = []
        for sec_num in suggested:
            if sec_num in self.sections:
                results.append({"section": sec_num, **self.sections[sec_num]})
        
        return sorted(results, key=lambda x: x["section"])
