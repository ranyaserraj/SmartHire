"""
Service d'extraction de données de CV - VERSION 2 ROBUSTE
Gère les CV complexes : tableaux, colonnes, formats variés
"""
import re
import io
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import pdfplumber
from PIL import Image
import pytesseract
from rapidfuzz import fuzz, process
from dateutil import parser as date_parser


class CVExtractorV2:
    """Extracteur de CV robuste avec support multi-format"""
    
    def __init__(self):
        # Patterns de dates multiples formats
        self.date_patterns = [
            # Format : Jan 2020, January 2020, Janvier 2020
            r'(?:jan(?:v(?:ier)?)?|fev(?:r(?:ier)?)?|mar(?:s)?|avr(?:il)?|mai|juin?|juil(?:let)?|aou(?:t)?|sep(?:t(?:embre)?)?|oct(?:obre)?|nov(?:embre)?|dec(?:embre)?|january|february|march|april|may|june|july|august|september|october|november|december)\.?\s*\d{4}',
            # Format : 03/2019, 12/2021
            r'\d{1,2}/\d{4}',
            # Format : 2019, 2020
            r'\b(?:19|20)\d{2}\b',
            # Format : Q1 2020, Q3 2021
            r'Q[1-4]\s*\d{4}',
        ]
        
        # Mots de fin de période
        self.end_period_words = [
            'present', 'aujourd\'hui', 'current', 'actuel', 'en cours',
            'now', 'ce jour', 'ongoing', 'toujours'
        ]
        
        # Sections avec variations (majuscules, minuscules, accents)
        self.section_patterns = {
            'experience': [
                r'exp[ée]riences?\s+professionnelles?',
                r'work\s+experience',
                r'professional\s+experience',
                r'employment\s+history',
                r'parcours\s+professionnel',
                r'historique\s+professionnel',
                r'carrière',
            ],
            'formation': [
                r'formations?',
                r'[ée]tudes',
                r'education',
                r'academic\s+background',
                r'scolarit[ée]',
                r'dipl[ôo]mes?',
                r'qualifications?',
            ],
            'competences': [
                r'comp[ée]tences?(?:\s+(?:techniques?|professionnelles?|cl[ée]s?))?',
                r'(?:technical|professional|core|key)?\s*skills?',
                r'expertise',
                r'ma[îi]trise',
                r'savoir[-\s]faire',
                r'competenc(?:ies|y)',
                r'areas?\s+of\s+expertise',
            ],
            'langues': [
                r'langues?',
                r'languages?',
            ],
            'profil': [
                r'profil',
                r'profile',
                r'summary',
                r'about\s+me',
                r'r[ée]sum[ée]',
                r'objectif',
                r'objective',
            ],
            'contact': [
                r'contacts?',
                r'coordonn[ée]es',
                r'informations?\s+personnelles?',
                r'personal\s+information',
            ]
        }
        
        # Compétences techniques étendues avec variations
        self.tech_skills_base = [
            # Langages
            'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'typescript', 'kotlin', 'swift', 'scala', 'r', 'matlab', 'perl', 'shell',
            # Frameworks web
            'react', 'angular', 'vue', 'vuejs', 'svelte', 'next', 'nextjs', 'nuxt',
            'django', 'flask', 'fastapi', 'spring', 'express', 'nodejs', 'node',
            'laravel', 'symfony', 'rails', 'asp.net', '.net',
            # Bases de données
            'sql', 'mysql', 'postgresql', 'postgres', 'mongodb', 'redis', 'oracle',
            'sqlite', 'mariadb', 'cassandra', 'elasticsearch', 'dynamodb',
            # DevOps & Cloud
            'docker', 'kubernetes', 'k8s', 'jenkins', 'gitlab', 'github', 'circleci',
            'aws', 'azure', 'gcp', 'google cloud', 'terraform', 'ansible', 'vagrant',
            # Data & AI
            'pandas', 'numpy', 'sklearn', 'tensorflow', 'pytorch', 'keras',
            'spark', 'hadoop', 'airflow', 'kafka', 'tableau', 'power bi',
            'machine learning', 'deep learning', 'nlp', 'computer vision',
            # Mobile
            'android', 'ios', 'react native', 'flutter', 'xamarin',
            # Autres
            'git', 'linux', 'unix', 'agile', 'scrum', 'jira', 'api', 'rest',
            'graphql', 'microservices', 'ci/cd', 'test', 'tdd', 'selenium',
        ]
        
        # Soft skills
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving',
            'analytical', 'creativity', 'adaptability', 'time management',
            'organization', 'critical thinking', 'collaboration', 'negotiation',
            'autonomie', 'travail d\'équipe', 'gestion du temps', 'créativité',
            'résolution de problèmes', 'esprit d\'équipe', 'organisation',
        ]
    
    def extract_from_file(self, file_path: str) -> Dict:
        """Point d'entrée principal - extrait selon le type de fichier"""
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            return self._extract_from_image(file_path)
        else:
            raise ValueError(f"Format non supporté : {file_path.suffix}")
    
    def _extract_from_pdf(self, file_path: Path) -> Dict:
        """Extraction robuste depuis PDF avec pdfplumber"""
        text = ""
        
        try:
            # Tentative 1 : pdfplumber (meilleur pour tableaux et colonnes)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # Extraire le texte
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    
                    # Si pas de texte, essayer d'extraire comme image (PDF scanné)
                    if not page_text or len(page_text.strip()) < 50:
                        # Convertir la page en image et appliquer OCR
                        try:
                            img = page.to_image(resolution=300)
                            pil_img = img.original
                            ocr_text = pytesseract.image_to_string(pil_img, lang='fra+eng')
                            if ocr_text and len(ocr_text.strip()) > 50:
                                text += ocr_text + "\n"
                        except Exception as e:
                            print(f"OCR fallback failed: {e}")
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}")
            # Fallback sur PyPDF2 si pdfplumber échoue
            try:
                import PyPDF2
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e2:
                print(f"PyPDF2 fallback failed: {e2}")
        
        # Si toujours pas de texte, OCR complet
        if not text or len(text.strip()) < 100:
            try:
                from pdf2image import convert_from_path
                images = convert_from_path(str(file_path))
                for img in images:
                    ocr_text = pytesseract.image_to_string(img, lang='fra+eng')
                    text += ocr_text + "\n"
            except Exception as e:
                print(f"Full OCR failed: {e}")
        
        return self._parse_cv_text(text)
    
    def _extract_from_image(self, file_path: Path) -> Dict:
        """Extraction depuis image avec OCR"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang='fra+eng')
            return self._parse_cv_text(text)
        except Exception as e:
            print(f"Image OCR failed: {e}")
            return self._empty_result()
    
    def _parse_cv_text(self, text: str) -> Dict:
        """Parse le texte du CV de manière intelligente"""
        if not text or len(text.strip()) < 50:
            return self._empty_result()
        
        # Normaliser le texte
        text = self._normalize_text(text)
        lines = text.split('\n')
        
        # Extraire les informations de contact (en-tête généralement)
        header_text = '\n'.join(lines[:20])  # Premiers 20 lignes
        
        nom = self._extract_name_robust(header_text, lines)
        email = self._extract_email(text)
        telephone = self._extract_phone(text)
        ville = self._extract_city(text)
        
        # Détection de sections avec contexte
        sections = self._detect_sections(lines)
        
        # Extraction par section
        competences = self._extract_skills_robust(text, sections.get('competences', []))
        experiences = self._extract_experiences_robust(text, sections.get('experience', []))
        formations = self._extract_education_robust(text, sections.get('formation', []))
        langues = self._extract_languages_robust(text, sections.get('langues', []))
        
        return {
            "nom": nom,
            "email": email,
            "telephone": telephone,
            "ville": ville,
            "competences_extraites": competences,
            "experience": experiences,
            "formation": formations,
            "langues": langues,
        }
    
    def _normalize_text(self, text: str) -> str:
        """Normalise le texte (espaces, sauts de ligne)"""
        # Supprimer les caractères de contrôle sauf \n
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        # Normaliser les espaces multiples
        text = re.sub(r' +', ' ', text)
        # Normaliser les sauts de ligne multiples
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    
    def _extract_name_robust(self, header_text: str, lines: List[str]) -> str:
        """Extraction robuste du nom avec NER-like approach"""
        # Chercher dans les 10 premières lignes
        for i, line in enumerate(lines[:10]):
            line = line.strip()
            if not line or len(line) < 3:
                continue
            
            # Skip si c'est une adresse, email, téléphone
            if re.search(r'@|\.com|\d{10}|\d{2}[/\s-]\d{2}', line):
                continue
            
            # Skip si c'est un titre de section
            if any(re.search(pattern, line, re.IGNORECASE) 
                   for patterns in self.section_patterns.values() 
                   for pattern in patterns):
                continue
            
            # Si ligne en majuscules ou avec premières lettres en maj
            if line.isupper() or line.istitle():
                # Vérifier qu'elle contient 2-4 mots
                words = line.split()
                if 2 <= len(words) <= 4:
                    # Vérifier que ce sont des mots (pas de chiffres, symboles)
                    if all(re.match(r'^[A-ZÀ-ÿa-z\'-]+$', word) for word in words):
                        return line.strip()
        
        return ""
    
    def _extract_email(self, text: str) -> str:
        """Extraction d'email robuste"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(pattern, text)
        return matches[0] if matches else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extraction de téléphone multi-format"""
        patterns = [
            # Format international : +XXX XXX XXX XXX
            r'\+\d{1,3}[\s.-]?\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{3,4}',
            # Format avec parenthèses : +XXX (XXX) XXX-XXXX
            r'\+?\d{1,3}[\s.-]?\(?\d{2,3}\)?[\s.-]?\d{3}[\s.-]?\d{4}',
            # Format standard : XXX-XXX-XXXX ou XXX.XXX.XXXX
            r'\d{3}[\s.-]\d{3}[\s.-]\d{4}',
            # Format marocain : 06XX XX XX XX ou +212 6XX XX XX XX
            r'(?:\+212|0)[5-7]\d{8}|(?:\+212|0)[5-7](?:[\s.-]?\d{2}){4}',
            # Format simple : 10 chiffres d'affilée
            r'\b\d{10}\b',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Nettoyer
                phone_clean = re.sub(r'[^\d+]', '', match)
                # Valider la longueur
                if 9 <= len(phone_clean) <= 15:
                    # Éviter les numéros qui ressemblent à des dates ou codes postaux
                    if not re.match(r'^(19|20)\d{2}', match):  # Pas une année
                        return match.strip()
        return ""
    
    def _extract_city(self, text: str) -> str:
        """Extraction de ville"""
        cities = [
            'Casablanca', 'Rabat', 'Fès', 'Marrakech', 'Tanger', 'Agadir',
            'Meknès', 'Oujda', 'Kenitra', 'Tétouan', 'Salé', 'Mohammedia',
            'Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice', 'Lille',
            'London', 'New York', 'Dubai', 'Montreal', 'Brussels',
        ]
        
        text_lower = text.lower()
        for city in cities:
            if city.lower() in text_lower:
                return city
        
        return ""
    
    def _detect_sections(self, lines: List[str]) -> Dict[str, List[str]]:
        """Détecte les sections et leur contenu avec contexte"""
        sections = {}
        current_section = None
        current_content = []
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Tester si c'est un titre de section
            section_detected = None
            for section_name, patterns in self.section_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, line_lower):
                        section_detected = section_name
                        break
                if section_detected:
                    break
            
            if section_detected:
                # Sauvegarder la section précédente
                if current_section and current_content:
                    sections[current_section] = current_content
                
                # Démarrer nouvelle section
                current_section = section_detected
                current_content = []
            elif current_section:
                # Ajouter à la section courante
                if line.strip():
                    current_content.append(line.strip())
        
        # Sauvegarder la dernière section
        if current_section and current_content:
            sections[current_section] = current_content
        
        return sections
    
    def _extract_skills_robust(self, text: str, section_lines: List[str]) -> List[str]:
        """Extraction de compétences avec fuzzy matching"""
        skills_found = set()
        
        # Mots à exclure (stopwords étendus)
        excluded_words = {
            # Mots communs anglais
            'the', 'and', 'for', 'with', 'from', 'this', 'that', 'these', 'those',
            'any', 'some', 'all', 'each', 'every', 'both', 'few', 'many', 'most',
            'other', 'such', 'only', 'own', 'same', 'than', 'too', 'very', 'can',
            'will', 'just', 'should', 'now', 'also', 'well', 'back', 'through',
            'where', 'much', 'before', 'after', 'here', 'there', 'when', 'how',
            'about', 'against', 'between', 'into', 'during', 'without', 'again',
            # Mots communs CV
            'profile', 'summary', 'work', 'experience', 'education', 'skills',
            'professional', 'relevant', 'interest', 'bachelor', 'master', 'degree',
            'university', 'college', 'school', 'year', 'month', 'date', 'city',
            'state', 'country', 'street', 'phone', 'email', 'address', 'contact',
            'assistant', 'manager', 'director', 'lead', 'senior', 'junior',
            'intern', 'coordinator', 'specialist', 'analyst', 'developer',
            'engineer', 'designer', 'consultant', 'supervisor', 'executive',
            # Mots français
            'profil', 'résumé', 'expérience', 'formation', 'compétences',
            'professionnelle', 'personnelle', 'année', 'mois', 'ville', 'pays',
            # Noms propres courants (à éviter)
            'january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            # Verbes d'action CV
            'managed', 'developed', 'created', 'designed', 'implemented', 'led',
            'coordinated', 'supervised', 'trained', 'analyzed', 'improved',
            'increased', 'decreased', 'achieved', 'completed', 'delivered',
            'ensured', 'maintained', 'supported', 'assisted', 'helped',
            'collaborated', 'worked', 'built', 'established', 'launched',
            'championed', 'propel', 'proven', 'highly', 'qualified',
            # Mots génériques
            'using', 'while', 'within', 'including', 'based', 'related',
            'various', 'multiple', 'several', 'different', 'specific',
            'general', 'overall', 'total', 'main', 'key', 'core', 'primary',
            # Acronymes de sections CV
            'st', 'rd', 'th', 'ave', 'blvd', 'apt', 'ste',
            # Autres
            'client', 'clients', 'company', 'companies', 'team', 'teams',
            'project', 'projects', 'program', 'programs', 'initiative', 'initiatives',
            'campaign', 'campaigns', 'event', 'events', 'task', 'tasks',
            'goal', 'goals', 'objective', 'objectives', 'strategy', 'strategies',
            'plan', 'plans', 'report', 'reports', 'document', 'documents',
            'presentation', 'presentations', 'meeting', 'meetings',
            'brochures', 'brochure', 'postcards', 'postcard', 'newsletter',
            'newsletters', 'press', 'release', 'releases', 'health', 'unlimited',
            'anywhere', 'everywhere', 'someone', 'something', 'anything',
        }
        
        # Texte à analyser : priorité à la section compétences
        section_text = ' '.join(section_lines)
        section_text_lower = section_text.lower()
        
        # Texte complet pour fallback
        full_text_lower = text.lower()
        
        # 1. Matching exact sur compétences techniques (dans section ET texte complet)
        for skill in self.tech_skills_base:
            # Chercher d'abord dans la section compétences
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', section_text_lower):
                skills_found.add(skill.title())
            # Sinon dans le texte complet
            elif re.search(r'\b' + re.escape(skill.lower()) + r'\b', full_text_lower):
                skills_found.add(skill.title())
        
        # 2. Extraction des acronymes et mots techniques UNIQUEMENT depuis la section compétences
        if section_lines:
            # Pattern pour acronymes techniques (2-15 caractères)
            tech_pattern = r'\b[A-Z][A-Za-z0-9\+\#\.]{1,14}\b'
            potential_skills = re.findall(tech_pattern, section_text)
            
            for skill in potential_skills:
                skill_lower = skill.lower()
                # Filtres stricts
                if (
                    skill_lower not in excluded_words and  # Pas dans les mots exclus
                    len(skill) >= 2 and  # Au moins 2 caractères
                    not skill.isdigit() and  # Pas un nombre
                    not re.match(r'^\d+$', skill) and  # Pas que des chiffres
                    not re.match(r'^[A-Z][a-z]+$', skill)  # Pas un mot normal (ex: "Lead", "Manager")
                ):
                    # Accepter uniquement les acronymes (tout en majuscules) ou avec caractères spéciaux
                    if skill.isupper() or any(c in skill for c in ['+', '#', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                        skills_found.add(skill)
        
        # 3. Soft skills (uniquement si mentionnés explicitement)
        for skill in self.soft_skills:
            if skill.lower() in section_text_lower or skill.lower() in full_text_lower:
                skills_found.add(skill.title())
        
        return sorted(list(skills_found))
    
    def _extract_experiences_robust(self, text: str, section_lines: List[str]) -> List[Dict]:
        """Extraction d'expériences avec parsing de dates avancé"""
        experiences = []
        
        if not section_lines:
            return experiences
        
        # Regrouper les lignes en blocs d'expérience (séparés par dates ou lignes vides)
        blocks = self._group_experience_blocks(section_lines)
        
        for block in blocks:
            exp = self._parse_experience_block(block)
            if exp:
                experiences.append(exp)
        
        return experiences
    
    def _group_experience_blocks(self, lines: List[str]) -> List[List[str]]:
        """Groupe les lignes en blocs d'expérience"""
        blocks = []
        current_block = []
        
        for line in lines:
            # Si ligne vide ou contient une date, possiblement nouveau bloc
            if not line.strip():
                if current_block:
                    blocks.append(current_block)
                    current_block = []
            else:
                current_block.append(line)
        
        if current_block:
            blocks.append(current_block)
        
        return blocks
    
    def _parse_experience_block(self, lines: List[str]) -> Optional[Dict]:
        """Parse un bloc d'expérience"""
        text = ' '.join(lines)
        
        # Extraire les dates
        dates = self._extract_dates_robust(text)
        if not dates:
            return None
        
        periode = self._format_date_range(dates)
        
        return {
            "periode": periode,
            "description": text[:300],  # Premier 300 caractères
        }
    
    def _extract_dates_robust(self, text: str) -> List[str]:
        """Extraction de dates multi-format"""
        dates = []
        
        # Chercher selon tous les patterns
        for pattern in self.date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        # Chercher les mots de fin de période
        for word in self.end_period_words:
            if word.lower() in text.lower():
                dates.append('Present')
        
        return dates[:2]  # Maximum 2 dates (début et fin)
    
    def _format_date_range(self, dates: List[str]) -> str:
        """Formate une plage de dates"""
        if not dates:
            return ""
        if len(dates) == 1:
            return dates[0]
        return f"{dates[0]} - {dates[1]}"
    
    def _extract_education_robust(self, text: str, section_lines: List[str]) -> List[Dict]:
        """Extraction de formation robuste"""
        education = []
        
        search_text = ' '.join(section_lines)
        
        # Diplômes étendus
        diplomas = {
            'Doctorat': ['doctorat', 'phd', 'ph.d', 'doctorate'],
            'Master': ['master', "master's", 'msc', 'm.sc', 'mastère'],
            'Ingénieur': ['ingénieur', 'engineer', 'engineering'],
            'Licence': ['licence', 'bachelor', 'bsc', 'b.sc', 'ba'],
            'DUT': ['dut'],
            'BTS': ['bts'],
            'MBA': ['mba'],
            'Bac': ['baccalauréat', 'bac +', 'high school'],
        }
        
        search_lower = search_text.lower()
        for diploma_name, variations in diplomas.items():
            for var in variations:
                if var in search_lower:
                    education.append({
                        "diplome": diploma_name,
                        "description": search_text[:200]
                    })
                    break
            if education:
                break
        
        return education
    
    def _extract_languages_robust(self, text: str, section_lines: List[str]) -> List[str]:
        """Extraction de langues robuste"""
        languages = set()
        
        search_text = ' '.join(section_lines) + ' ' + text
        search_lower = search_text.lower()
        
        lang_variations = {
            'Français': ['français', 'francais', 'french'],
            'Anglais': ['anglais', 'english'],
            'Arabe': ['arabe', 'arabic'],
            'Espagnol': ['espagnol', 'spanish'],
            'Allemand': ['allemand', 'german'],
            'Italien': ['italien', 'italian'],
            'Portugais': ['portugais', 'portuguese'],
            'Chinois': ['chinois', 'chinese', 'mandarin'],
            'Japonais': ['japonais', 'japanese'],
            'Russe': ['russe', 'russian'],
        }
        
        for lang_name, variations in lang_variations.items():
            if any(var in search_lower for var in variations):
                languages.add(lang_name)
        
        return sorted(list(languages))
    
    def _empty_result(self) -> Dict:
        """Résultat vide"""
        return {
            "nom": "",
            "email": "",
            "telephone": "",
            "ville": "",
            "competences_extraites": [],
            "experience": [],
            "formation": [],
            "langues": [],
        }


# Instance globale
extractor_v2 = CVExtractorV2()

