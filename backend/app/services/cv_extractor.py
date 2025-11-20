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
        
        # Mots-clés pour sections (français + anglais)
        self.section_keywords = {
            'experience': [
                # Français
                'expérience', 'experience', 'expériences', 'experiences',
                'parcours professionnel', 'carrière', 'historique professionnel',
                # Anglais
                'work experience', 'professional experience', 'employment history',
                'career history', 'work history'
            ],
            'formation': [
                # Français
                'formation', 'formations', 'études', 'diplôme', 'diplômes', 'scolarité',
                # Anglais
                'education', 'academic background', 'qualifications', 'degrees'
            ],
            'competences': [
                # Français
                'compétence', 'compétences', 'expertise', 'maîtrise', 'savoir-faire',
                'compétences techniques', 'compétences professionnelles',
                # Anglais
                'skills', 'skill', 'technical skills', 'professional skills',
                'core competencies', 'key skills', 'areas of expertise',
                'technical competencies', 'soft skills', 'hard skills'
            ],
            'langues': [
                # Français
                'langue', 'langues',
                # Anglais
                'languages', 'language'
            ],
            'contact': [
                # Français
                'contact', 'coordonnées', 'informations personnelles',
                # Anglais
                'contact information', 'personal information', 'contact details'
            ]
        }
        
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
        # Identifier les sections du CV
        sections = self._identify_sections(text)
        
        # Extraire le header (premières lignes avant les sections)
        header = sections.get('header', text[:500])
        
        result = {
            "nom_complet": self._extract_name_from_header(header, text),
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
    
    def _extract_name_from_header(self, header: str, full_text: str) -> Optional[str]:
        """Extrait le nom depuis le header du CV"""
        lines = header.strip().split('\n')
        lines = [l.strip() for l in lines if l.strip()]
        
        if not lines:
            return self._extract_name(full_text)
        
        # Stratégie: Le nom est souvent la première ou deuxième ligne significative
        for i, line in enumerate(lines[:5]):
            words = line.split()
            
            # Ignorer les lignes avec email, téléphone ou URLs
            if any(char in line for char in ['@', 'http', 'www']):
                continue
            
            # Ignorer les lignes avec des chiffres (probablement téléphone ou date)
            if re.search(r'\d{4,}', line):
                continue
            
            # Le nom: 2-4 mots, pas trop long
            if 2 <= len(words) <= 4 and 5 <= len(line) <= 50:
                # Tous les mots commencent par une majuscule ou tout en majuscules
                if line.isupper():
                    return ' '.join([w.capitalize() for w in words])
                elif all(w[0].isupper() for w in words if w and w[0].isalpha()):
                    return line
        
        # Fallback à l'ancienne méthode
        return self._extract_name(full_text)
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identifie les différentes sections du CV"""
        sections = {}
        lines = text.split('\n')
        current_section = 'header'
        section_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Vérifier si c'est un titre de section
            is_section_title = False
            for section_type, keywords in self.section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    # Sauvegarder la section précédente
                    if section_content:
                        sections[current_section] = '\n'.join(section_content)
                    
                    # Commencer une nouvelle section
                    current_section = section_type
                    section_content = []
                    is_section_title = True
                    break
            
            if not is_section_title and line.strip():
                section_content.append(line)
        
        # Sauvegarder la dernière section
        if section_content:
            sections[current_section] = '\n'.join(section_content)
        
        return sections
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Extrait le nom (généralement dans les premières lignes)"""
        lines = text.strip().split('\n')
        
        # Nettoyer les lignes vides
        lines = [l.strip() for l in lines if l.strip()]
        
        # Stratégie 1: Chercher dans les 10 premières lignes
        for i, line in enumerate(lines[:10]):
            # Le nom est souvent composé de 2-4 mots
            words = line.split()
            if 2 <= len(words) <= 4 and len(line) < 50:
                # Vérifier que ce n'est pas un email, téléphone ou URL
                if (not re.search(self.email_pattern, line) and 
                    not re.search(self.phone_pattern, line) and
                    not 'http' in line.lower() and
                    not '@' in line):
                    
                    # Si ligne en majuscules et ressemble à un nom
                    if line.isupper():
                        return ' '.join([w.capitalize() for w in words])
                    
                    # Si la première ligne non vide ressemble à un nom (commence par majuscule)
                    if i < 3 and all(w[0].isupper() for w in words if w):
                        # Pas un titre de section commun
                        lower_line = line.lower()
                        if not any(keyword in lower_line for keyword in 
                                 ['expérience', 'formation', 'compétence', 'contact', 
                                  'objectif', 'profil', 'curriculum']):
                            return line
        
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extrait l'adresse email"""
        emails = re.findall(self.email_pattern, text)
        return emails[0] if emails else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extrait le numéro de téléphone"""
        # Patterns pour téléphones marocains
        patterns = [
            r'\+212[\s-]?[5-7][\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}',  # +212 6 XX XX XX XX
            r'0[5-7][\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}',  # 06 XX XX XX XX
            r'\+212[\s-]?\d{9}',  # +212XXXXXXXXX
            r'0[5-7]\d{8}',  # 06XXXXXXXX
        ]
        
        for pattern in patterns:
            phones = re.findall(pattern, text)
            if phones:
                phone = phones[0]
                # Nettoyer et normaliser
                phone = re.sub(r'[-\s]', '', phone)
                if phone.startswith('0'):
                    phone = '+212' + phone[1:]
                elif not phone.startswith('+'):
                    phone = '+212' + phone
                return phone
        
        return None
    
    def _extract_city(self, text: str) -> Optional[str]:
        """Extrait la ville"""
        moroccan_cities = [
            'Casablanca', 'Rabat', 'Marrakech', 'Fès', 'Fes', 'Tanger', 'Agadir',
            'Meknès', 'Meknes', 'Oujda', 'Kenitra', 'Kénitra', 'Tétouan', 'Tetouan',
            'Salé', 'Sale', 'Mohammedia', 'El Jadida', 'Khouribga', 'Beni Mellal',
            'Nador', 'Settat', 'Safi', 'Essaouira', 'Larache', 'Khemisset'
        ]
        
        text_lower = text.lower()
        lines = text.split('\n')
        
        # Chercher dans les 15 premières lignes (section contact/header)
        for line in lines[:15]:
            line_lower = line.lower().strip()
            for city in moroccan_cities:
                if city.lower() in line_lower:
                    # Vérifier que c'est bien la ville et pas dans un contexte différent
                    if len(line.split()) <= 10:  # Ligne courte, probablement contact
                        return city
        
        # Chercher dans tout le texte si pas trouvé
        for city in moroccan_cities:
            if city.lower() in text_lower:
                return city
        
        return None
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extrait les compétences techniques"""
        skills_keywords = [
            # Langages de programmation
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby',
            'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab',
            # Frameworks & Libraries
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'fastapi',
            'spring', 'laravel', 'express', 'next.js', 'nuxt',
            # Bases de données
            'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'oracle', 'sqlserver',
            'cassandra', 'elasticsearch',
            # DevOps & Cloud
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'gitlab', 'github',
            'terraform', 'ansible', 'ci/cd',
            # Web
            'html', 'css', 'tailwind', 'bootstrap', 'sass', 'less', 'webpack',
            # Méthodologies
            'agile', 'scrum', 'kanban', 'devops',
            # Compétences RH spécifiques (français)
            'recrutement', 'formation', 'paie', 'sirh', 'droit du travail',
            'gestion des talents', 'onboarding', 'évaluation', 'communication',
            'résolution de conflits', 'négociation', 'leadership', 'coaching',
            # Compétences RH (anglais)
            'recruitment', 'recruiting', 'talent management', 'hr management',
            'payroll', 'compensation', 'benefits', 'employee relations',
            'performance management', 'training', 'conflict resolution',
            # Outils
            'git', 'jira', 'confluence', 'slack', 'teams', 'excel', 'powerpoint',
            'word', 'office', 'sap', 'workday', 'bamboohr',
            # Autres
            'api', 'rest', 'graphql', 'microservices', 'machine learning', 
            'data science', 'ai', 'intelligence artificielle', 'big data',
            'analytics', 'bi', 'power bi', 'tableau'
        ]
        
        found_skills = []
        text_lower = text.lower()
        lines = text.split('\n')
        
        # Chercher la section "COMPÉTENCES" ou "SKILLS" ou similaire
        competences_section = ""
        in_competences = False
        section_keywords = [
            # Français
            'compétence', 'compétences', 'expertise', 'maîtrise', 'savoir-faire',
            # Anglais
            'skills', 'skill', 'technical skills', 'professional skills',
            'core competencies', 'key skills', 'competencies'
        ]
        stop_keywords = [
            # Français
            'expérience', 'formation', 'langue', 'contact', 'éducation', 'études',
            # Anglais
            'experience', 'education', 'languages', 'contact', 'work history'
        ]
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Détecter le début de la section compétences
            if any(keyword in line_lower for keyword in section_keywords):
                in_competences = True
                continue
            
            # Détecter la fin de la section
            if in_competences and any(keyword in line_lower for keyword in stop_keywords):
                break
            
            # Collecter les lignes de la section compétences
            if in_competences and line.strip():
                competences_section += " " + line
        
        # Si on a trouvé une section compétences, chercher dedans en priorité
        search_text = competences_section if competences_section else text_lower
        
        # Extraire les compétences connues
        for skill in skills_keywords:
            if skill in search_text:
                found_skills.append(skill.capitalize())
        
        # Nettoyer et retourner sans doublons
        return list(set(found_skills))
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extrait les expériences professionnelles"""
        experiences = []
        
        # Rechercher les sections d'expérience (français + anglais)
        experience_patterns = [
            # Français
            r'expérience professionnelle',
            r'expériences professionnelles',
            r'experience',
            r'experiences',
            r'parcours professionnel',
            # Anglais
            r'work experience',
            r'professional experience',
            r'employment history',
            r'career history'
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
                        "periode": f"{dates[0]} - {dates[-1] if len(dates) > 1 else 'Present'}",
                        "description": section[:200]
                    })
                break
        
        return experiences
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extrait la formation"""
        education = []
        
        # Rechercher les sections de formation (français + anglais)
        education_patterns = [
            # Français
            r'formation',
            r'formations',
            r'études',
            r'diplômes',
            r'diplôme',
            # Anglais
            r'education',
            r'academic background',
            r'qualifications'
        ]
        
        text_lower = text.lower()
        for pattern in education_patterns:
            if pattern in text_lower:
                start_idx = text_lower.find(pattern)
                section = text[start_idx:start_idx + 400]
                
                # Rechercher les diplômes communs (français + anglais)
                diplomas = {
                    'master': ['master', "master's", 'msc', 'm.sc'],
                    'licence': ['licence', 'bachelor', 'bsc', 'b.sc', 'ba'],
                    'bac': ['baccalauréat', 'bac', 'high school'],
                    'ingénieur': ['ingénieur', 'engineer', 'engineering degree'],
                    'doctorat': ['doctorat', 'phd', 'doctorate', 'ph.d'],
                    'dut': ['dut'],
                    'bts': ['bts'],
                    'mba': ['mba'],
                    'dea': ['dea', 'dess']
                }
                
                for diploma_name, variations in diplomas.items():
                    if any(var in text_lower for var in variations):
                        education.append({
                            "diplome": diploma_name.title(),
                            "description": section[:150]
                        })
                        break
                break
        
        return education
    
    def _extract_languages(self, text: str) -> List[str]:
        """Extrait les langues"""
        languages = []
        # Langues en français et anglais
        common_languages = {
            'français': ['français', 'francais', 'french'],
            'anglais': ['anglais', 'english'],
            'arabe': ['arabe', 'arabic'],
            'espagnol': ['espagnol', 'spanish'],
            'allemand': ['allemand', 'german'],
            'italien': ['italien', 'italian'],
            'portugais': ['portugais', 'portuguese'],
            'chinois': ['chinois', 'chinese', 'mandarin'],
            'japonais': ['japonais', 'japanese'],
            'russe': ['russe', 'russian']
        }
        
        text_lower = text.lower()
        for lang_fr, variations in common_languages.items():
            if any(var in text_lower for var in variations):
                languages.append(lang_fr.title())
        
        return list(set(languages))  # Éviter les doublons
    
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

