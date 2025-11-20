"""Service pour extraire les informations d'un CV"""
import re
from typing import Dict, List, Optional
import PyPDF2
from PIL import Image
import pytesseract
import json


class CVExtractor:
    """Extrait les informations structurées d'un CV"""
    
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(?:\+212|0)[5-7]\d{8}'
        
    def extract_from_pdf(self, file_path: str) -> Dict:
        """Extrait le texte et les informations d'un PDF"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return self._create_empty_result()
        
        return self._parse_cv_text(text)
    
    def extract_from_image(self, file_path: str) -> Dict:
        """Extrait le texte et les informations d'une image avec OCR"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang='fra+eng')
        except Exception as e:
            print(f"Error extracting from image: {e}")
            return self._create_empty_result()
        
        return self._parse_cv_text(text)
    
    def _parse_cv_text(self, text: str) -> Dict:
        """Parse le texte du CV pour extraire les informations structurées"""
        result = {
            "nom_complet": self._extract_name(text),
            "email": self._extract_email(text),
            "telephone": self._extract_phone(text),
            "ville": self._extract_city(text),
            "competences": self._extract_skills(text),
            "experience": self._extract_experience(text),
            "formation": self._extract_education(text),
            "langues": self._extract_languages(text),
            "contenu_texte": text
        }
        return result
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Extrait le nom (généralement dans les premières lignes)"""
        lines = text.strip().split('\n')
        # Le nom est souvent dans les 3 premières lignes en majuscules
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 0 and len(line) < 50:
                # Si la ligne contient surtout des majuscules et des espaces
                if line.isupper() or len(line.split()) <= 3:
                    # Vérifier que ce n'est pas un email ou téléphone
                    if not re.search(self.email_pattern, line) and not re.search(self.phone_pattern, line):
                        return line.title()
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extrait l'adresse email"""
        emails = re.findall(self.email_pattern, text)
        return emails[0] if emails else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extrait le numéro de téléphone"""
        phones = re.findall(self.phone_pattern, text)
        if phones:
            phone = phones[0]
            # Normaliser le format
            phone = re.sub(r'\s+', '', phone)
            if phone.startswith('0'):
                phone = '+212' + phone[1:]
            return phone
        return None
    
    def _extract_city(self, text: str) -> Optional[str]:
        """Extrait la ville"""
        moroccan_cities = [
            'Casablanca', 'Rabat', 'Marrakech', 'Fès', 'Tanger', 'Agadir',
            'Meknès', 'Oujda', 'Kenitra', 'Tétouan', 'Salé', 'Mohammedia',
            'El Jadida', 'Khouribga', 'Beni Mellal', 'Nador'
        ]
        
        text_lower = text.lower()
        for city in moroccan_cities:
            if city.lower() in text_lower:
                return city
        return None
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extrait les compétences techniques"""
        skills_keywords = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node.js', 'django', 'flask', 'fastapi', 'sql', 'postgresql', 'mysql',
            'mongodb', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git',
            'html', 'css', 'tailwind', 'bootstrap', 'agile', 'scrum', 'api',
            'rest', 'graphql', 'machine learning', 'data science', 'ai'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skills_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extrait les expériences professionnelles"""
        experiences = []
        
        # Rechercher les sections d'expérience
        experience_patterns = [
            r'expérience professionnelle',
            r'experience',
            r'parcours professionnel'
        ]
        
        text_lower = text.lower()
        for pattern in experience_patterns:
            if pattern in text_lower:
                # Extraire la section (simplifié)
                start_idx = text_lower.find(pattern)
                section = text[start_idx:start_idx + 500]
                
                # Rechercher les dates (format YYYY ou MM/YYYY)
                date_pattern = r'\b(20\d{2}|19\d{2})\b'
                dates = re.findall(date_pattern, section)
                
                if dates:
                    experiences.append({
                        "periode": f"{dates[0]} - {dates[-1] if len(dates) > 1 else 'Présent'}",
                        "description": section[:200]
                    })
                break
        
        return experiences
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extrait la formation"""
        education = []
        
        # Rechercher les sections de formation
        education_patterns = [
            r'formation',
            r'études',
            r'diplômes',
            r'education'
        ]
        
        text_lower = text.lower()
        for pattern in education_patterns:
            if pattern in text_lower:
                start_idx = text_lower.find(pattern)
                section = text[start_idx:start_idx + 400]
                
                # Rechercher les diplômes communs
                diplomas = ['master', 'licence', 'bac', 'ingénieur', 'doctorat', 'dut', 'bts']
                for diploma in diplomas:
                    if diploma in text_lower:
                        education.append({
                            "diplome": diploma.title(),
                            "description": section[:150]
                        })
                        break
                break
        
        return education
    
    def _extract_languages(self, text: str) -> List[str]:
        """Extrait les langues"""
        languages = []
        common_languages = ['français', 'anglais', 'arabe', 'espagnol', 'allemand']
        
        text_lower = text.lower()
        for lang in common_languages:
            if lang in text_lower:
                languages.append(lang.title())
        
        return languages
    
    def _create_empty_result(self) -> Dict:
        """Crée un résultat vide en cas d'erreur"""
        return {
            "nom_complet": None,
            "email": None,
            "telephone": None,
            "ville": None,
            "competences": [],
            "experience": [],
            "formation": [],
            "langues": [],
            "contenu_texte": ""
        }

