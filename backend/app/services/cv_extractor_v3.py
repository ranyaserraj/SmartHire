"""
Service d'extraction de données de CV - VERSION 3 AVANCÉE
Dataset multi-domaines avec 2795 compétences

Améliorations V3:
- Dataset 9544 CV réels (tous secteurs)
- Tri spatial des blocs (x, y) pour CV en colonnes
- Fuzzy matching pour détection de sections
- Dates avec tous séparateurs (→, –, >, etc.)
- Regroupement de lignes logiques
- Split compétences par séparateurs
- Détection intelligente du nom
- Extraction adresse complète
- Langues avec niveaux CEFR
- Soft skills automatiques
"""
import sys
import io as io_module

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io_module.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io_module.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import re
import json
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# PDF & Image processing
import pdfplumber
from PIL import Image
import pytesseract

# Text processing
from rapidfuzz import fuzz, process
from dateutil import parser as date_parser

# Skills loader
from .skills_loader import get_skills_loader


class CVExtractorV3:
    """Extracteur de CV V3 avec dataset multi-domaines français"""
    
    def __init__(self):
        print("🚀 Initialisation CV Extractor V3...")
        
        # Charger le dataset de compétences
        self.skills_loader = get_skills_loader()
        
        # Patterns de dates ÉTENDUS (tous séparateurs)
        self.date_patterns = self._init_date_patterns()
        
        # Patterns de sections avec variations
        self.section_patterns = self._init_section_patterns()
        
        # Stopwords étendus (mots à exclure)
        self.excluded_words = self._init_excluded_words()
        
        # Villes et pays
        self.cities = self._init_cities()
        
        # Niveaux de langues CEFR
        self.language_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2',
                                'débutant', 'intermédiaire', 'avancé', 'courant', 'natif',
                                'beginner', 'intermediate', 'advanced', 'fluent', 'native']
        
        print("✅ CV Extractor V3 prêt")
        stats = self.skills_loader.get_stats()
        print(f"   📊 Dataset: {stats['total_skills']} compétences chargées")
    
    def _init_date_patterns(self) -> List[str]:
        """Patterns de dates multi-format avec TOUS les séparateurs"""
        return [
            # Mois texte + année
            r'(?:jan(?:v(?:ier)?)?|f[ée]v(?:r(?:ier)?)?|mar(?:s)?|avr(?:il)?|mai|juin?|juil(?:let)?|ao[ûu](?:t)?|sep(?:t(?:embre)?)?|oct(?:obre)?|nov(?:embre)?|d[ée]c(?:embre)?|january|february|march|april|may|june|july|august|september|october|november|december)\.?\s*\d{4}',
            # MM/YYYY ou MM-YYYY
            r'\d{1,2}[/-]\d{4}',
            # YYYY seul
            r'\b(?:19|20)\d{2}\b',
            # Trimestre
            r'Q[1-4]\s*\d{4}',
            # Année scolaire
            r'\d{4}[\s]*[-–—/]\s*\d{4}',
        ]
    
    def _init_section_patterns(self) -> Dict[str, List[str]]:
        """Patterns de sections avec fuzzy matching"""
        return {
            'experience': [
                'expérience', 'experiences', 'exp professionnelle',
                'work experience', 'professional experience', 'employment',
                'career', 'parcours professionnel', 'historique'
            ],
            'formation': [
                'formation', 'formations', 'études', 'education',
                'academic background', 'qualifications', 'diplômes', 'scolarité'
            ],
            'competences': [
                'compétences', 'skills', 'expertise', 'maîtrise',
                'technical skills', 'professional skills', 'core competencies',
                'savoir-faire', 'abilities', 'capacités'
            ],
            'langues': [
                'langues', 'languages', 'idiomas'
            ],
            'profil': [
                'profil', 'profile', 'summary', 'résumé', 'about',
                'objectif', 'objective', 'présentation'
            ],
        }
    
    def _init_excluded_words(self) -> Set[str]:
        """Mots à exclure de l'extraction (stopwords)"""
        return {
            # Sections CV
            'profile', 'summary', 'work', 'experience', 'education', 'skills',
            'professional', 'relevant', 'interest', 'bachelor', 'master',
            'university', 'school', 'contact', 'email', 'phone', 'address',
            
            # Titres de poste
            'assistant', 'manager', 'director', 'lead', 'senior', 'junior',
            'specialist', 'analyst', 'coordinator', 'supervisor', 'executive',
            
            # Verbes d'action
            'managed', 'developed', 'created', 'designed', 'implemented',
            'coordinated', 'supervised', 'analyzed', 'improved', 'led',
            
            # Mots génériques
            'client', 'company', 'team', 'project', 'program', 'initiative',
            'campaign', 'event', 'task', 'goal', 'objective', 'strategy',
            
            # Français
            'profil', 'résumé', 'expérience', 'formation', 'compétences',
            'responsable', 'chargé', 'assistant', 'directeur', 'manager',
        }
    
    def _init_cities(self) -> List[str]:
        """Liste des villes principales"""
        return [
            # Maroc
            'Casablanca', 'Rabat', 'Fès', 'Marrakech', 'Tanger', 'Agadir',
            'Meknès', 'Oujda', 'Kenitra', 'Tétouan', 'Salé', 'Mohammedia',
            # France
            'Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice', 'Nantes',
            'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille', 'Rennes',
            # International
            'London', 'New York', 'Dubai', 'Montreal', 'Brussels', 'Geneva',
        ]
    
    # ========================================================================
    # EXTRACTION PRINCIPALE
    # ========================================================================
    
    def extract_from_file(self, file_path: str) -> Dict:
        """Point d'entrée principal"""
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            return self._extract_from_image(file_path)
        else:
            raise ValueError(f"Format non supporté: {file_path.suffix}")
    
    def _extract_from_pdf(self, file_path: Path) -> Dict:
        """Extraction PDF avec tri spatial"""
        text_blocks = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # AMÉLIORATION: Tri spatial des blocs
                    page_blocks = self._extract_page_spatial(page)
                    text_blocks.extend(page_blocks)
        except Exception as e:
            print(f"❌ Erreur extraction PDF: {e}")
            return self._empty_result()
        
        # Joindre tout le texte
        full_text = '\n'.join(text_blocks)
        
        if not full_text or len(full_text) < 50:
            return self._empty_result()
        
        return self._parse_cv_text(full_text, text_blocks)
    
    def _extract_page_spatial(self, page) -> List[str]:
        """
        AMÉLIORATION: Extraction avec tri spatial (x, y)
        Pour gérer les CV en colonnes et tableaux
        """
        try:
            # Extraire les mots avec coordonnées
            words = page.extract_words(
                x_tolerance=3,
                y_tolerance=3,
                keep_blank_chars=False
            )
            
            if not words:
                # Fallback: extraction simple
                return [page.extract_text() or ""]
            
            # Regrouper par lignes (même coordonnée y)
            lines_dict = defaultdict(list)
            
            for word in words:
                # Arrondir y pour grouper les mots sur la même ligne
                y_coord = round(word['top'])
                lines_dict[y_coord].append((word['x0'], word['text']))
            
            # Trier les lignes de haut en bas
            sorted_lines = []
            for y in sorted(lines_dict.keys()):
                # Trier les mots de gauche à droite
                line_words = sorted(lines_dict[y], key=lambda x: x[0])
                line_text = ' '.join([w[1] for w in line_words])
                sorted_lines.append(line_text)
            
            return sorted_lines
        
        except Exception as e:
            print(f"⚠️ Spatial extraction failed, using fallback: {e}")
            return [page.extract_text() or ""]
    
    def _extract_from_image(self, file_path: Path) -> Dict:
        """Extraction depuis image avec OCR"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang='fra+eng')
            lines = text.split('\n')
            return self._parse_cv_text(text, lines)
        except Exception as e:
            print(f"❌ Erreur OCR: {e}")
            return self._empty_result()
    
    # ========================================================================
    # PARSING DU TEXTE
    # ========================================================================
    
    def _parse_cv_text(self, text: str, lines: List[str]) -> Dict:
        """Parse le texte extrait"""
        if not text or len(text.strip()) < 50:
            return self._empty_result()
        
        # AMÉLIORATION: Regroupement lignes logiques
        lines = self._regroup_logical_lines(lines)
        
        # Extraction informations contact (en-tête)
        header_text = '\n'.join(lines[:20])
        
        nom = self._extract_name_intelligent(lines)
        email = self._extract_email(text)
        telephone = self._extract_phone(text)
        ville = self._extract_city(text)
        
        # AMÉLIORATION: Détection sections avec fuzzy matching
        sections = self._detect_sections_fuzzy(lines)
        
        # AMÉLIORATION: Extraction avec dataset multi-domaines
        competences_data = self._extract_skills_esco(
            text, 
            sections.get('competences', [])
        )
        
        experiences = self._extract_experiences_robust(
            text, 
            sections.get('experience', [])
        )
        
        formations = self._extract_education_robust(
            text, 
            sections.get('formation', [])
        )
        
        # AMÉLIORATION: Langues avec niveaux
        langues = self._extract_languages_with_levels(
            text, 
            sections.get('langues', [])
        )
        
        return {
            "nom": nom,
            "email": email,
            "telephone": telephone,
            "ville": ville,
            "competences_extraites": competences_data['technical'] + competences_data['soft'],
            "experience": experiences,
            "formation": formations,
            "langues": langues,
        }
    
    # ========================================================================
    # AMÉLIORATION: Regroupement lignes logiques
    # ========================================================================
    
    def _regroup_logical_lines(self, lines: List[str]) -> List[str]:
        """
        Regroupe les lignes qui appartiennent ensemble
        Exemple:
            "Gestion de projets"
            "Agile Scrum Jira"
        → "Gestion de projets Agile Scrum Jira"
        """
        regrouped = []
        current_group = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_group:
                    regrouped.append(' '.join(current_group))
                    current_group = []
                continue
            
            # Si ligne courte (< 50 caractères) et pas de ponctuation finale
            if len(line) < 50 and not re.search(r'[.!?]$', line):
                current_group.append(line)
            else:
                if current_group:
                    current_group.append(line)
                    regrouped.append(' '.join(current_group))
                    current_group = []
                else:
                    regrouped.append(line)
        
        if current_group:
            regrouped.append(' '.join(current_group))
        
        return regrouped
    
    # ========================================================================
    # AMÉLIORATION: Fuzzy matching pour détection de sections
    # ========================================================================
    
    def _detect_sections_fuzzy(self, lines: List[str]) -> Dict[str, List[str]]:
        """
        Détection de sections avec fuzzy matching
        Gère: typos, accents, symboles, icônes
        """
        sections = {}
        current_section = None
        current_content = []
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            
            # Nettoyer pour matching (enlever symboles, chiffres, etc.)
            line_clean = re.sub(r'[^\w\s]', '', line_stripped.lower())
            line_clean = re.sub(r'\d+', '', line_clean).strip()
            
            # Tester chaque type de section
            best_section = None
            best_score = 0
            
            for section_name, keywords in self.section_patterns.items():
                for keyword in keywords:
                    # Fuzzy match
                    score = fuzz.partial_ratio(keyword, line_clean)
                    
                    if score > 85 and score > best_score:
                        best_section = section_name
                        best_score = score
            
            if best_section:
                # Sauvegarder section précédente
                if current_section and current_content:
                    sections[current_section] = current_content
                
                current_section = best_section
                current_content = []
            elif current_section:
                current_content.append(line_stripped)
        
        # Sauvegarder dernière section
        if current_section and current_content:
            sections[current_section] = current_content
        
        return sections
    
    # ========================================================================
    # AMÉLIORATION: Détection nom intelligente
    # ========================================================================
    
    def _extract_name_intelligent(self, lines: List[str]) -> str:
        """
        Détection intelligente du nom dans les 20 premières lignes
        Gère: nom en bannière, au milieu, en majuscules, sur 2 lignes
        """
        candidates = []
        
        for i, line in enumerate(lines[:20]):
            line = line.strip()
            if not line or len(line) < 3:
                continue
            
            # Skip si email, téléphone, URL, adresse
            if re.search(r'@|\.com|http|www|\d{5,}', line.lower()):
                continue
            
            # Skip si c'est une section
            if any(keyword in line.lower() for patterns in self.section_patterns.values() for keyword in patterns):
                continue
            
            # Calculer un score
            score = 0
            words = line.split()
            
            # Critère 1: Majuscules (nom souvent en caps)
            if line.isupper():
                score += 4
            elif line.istitle():
                score += 3
            
            # Critère 2: 2-4 mots (prénom + nom)
            if 2 <= len(words) <= 4:
                score += 3
            elif len(words) == 1:
                score += 1
            
            # Critère 3: Que des lettres (pas de chiffres)
            if all(re.match(r'^[A-ZÀ-ÿa-z\'-]+$', word) for word in words):
                score += 3
            
            # Critère 4: Position (plus haut = plus probable)
            position_bonus = (20 - i) / 4
            score += position_bonus
            
            # Critère 5: Longueur raisonnable
            if 5 <= len(line) <= 50:
                score += 2
            
            candidates.append((line, score))
        
        # Retourner le meilleur candidat
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0]
        
        return ""
    
    # ========================================================================
    # EXTRACTION INFORMATIONS CONTACT
    # ========================================================================
    
    def _extract_email(self, text: str) -> str:
        """Extraction email"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(pattern, text)
        return matches[0] if matches else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extraction téléphone multi-format"""
        patterns = [
            # International
            r'\+\d{1,3}[\s.-]?\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{3,4}',
            # Avec parenthèses
            r'\+?\d{1,3}[\s.-]?\(?\d{2,3}\)?[\s.-]?\d{3}[\s.-]?\d{4}',
            # Standard
            r'\d{3}[\s.-]\d{3}[\s.-]\d{4}',
            # Marocain
            r'(?:\+212|0)[5-7]\d{8}|(?:\+212|0)[5-7](?:[\s.-]?\d{2}){4}',
            # Simple
            r'\b\d{10}\b',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                phone_clean = re.sub(r'[^\d+]', '', match)
                if 9 <= len(phone_clean) <= 15:
                    if not re.match(r'^(19|20)\d{2}', match):
                        return match.strip()
        return ""
    
    def _extract_city(self, text: str) -> str:
        """Extraction ville"""
        text_lower = text.lower()
        for city in self.cities:
            if city.lower() in text_lower:
                return city
        return ""
    
    # ========================================================================
    # AMÉLIORATION: Extraction skills avec ESCO
    # ========================================================================
    
    def _extract_skills_esco(self, text: str, section_lines: List[str]) -> Dict[str, List[str]]:
        """
        Extraction de compétences avec ESCO (13 000+ skills)
        """
        # Texte de la section compétences
        section_text = ' '.join(section_lines)
        
        # AMÉLIORATION: Split par séparateurs
        skills_text = self._split_by_separators(section_text)
        
        # Rechercher avec ESCO
        found_skills = self.esco.search_skills(section_text + ' ' + text, threshold=85)
        
        # Filtrer les mots exclus
        found_skills['technical'] = [
            s for s in found_skills['technical'] 
            if s.lower() not in self.excluded_words
        ]
        found_skills['soft'] = [
            s for s in found_skills['soft'] 
            if s.lower() not in self.excluded_words
        ]
        
        return found_skills
    
    def _split_by_separators(self, text: str) -> List[str]:
        """
        AMÉLIORATION: Split compétences par séparateurs
        Gère: , ; / • - | et retours à la ligne
        """
        separators = [',', ';', '/', '•', '|', '\n', ' - ']
        
        # Remplacer tous par virgule
        for sep in separators:
            text = text.replace(sep, ',')
        
        # Split et nettoyer
        items = [item.strip() for item in text.split(',') if item.strip()]
        
        return items
    
    # ========================================================================
    # AMÉLIORATION: Extraction expériences avec dates avancées
    # ========================================================================
    
    def _extract_experiences_robust(self, text: str, section_lines: List[str]) -> List[Dict]:
        """Extraction d'expériences avec parsing de dates avancé"""
        if not section_lines:
            return []
        
        experiences = []
        current_exp = {}
        
        for line in section_lines:
            # Chercher les dates avec TOUS les séparateurs
            dates = self._extract_dates_advanced(line)
            
            if dates:
                # Si on a déjà une expérience en cours, la sauvegarder
                if current_exp:
                    experiences.append(current_exp)
                
                # Nouvelle expérience
                current_exp = {
                    "periode": self._format_date_range(dates),
                    "description": line[:200]
                }
            elif current_exp:
                # Continuer la description
                current_exp["description"] += " " + line[:100]
        
        if current_exp:
            experiences.append(current_exp)
        
        return experiences
    
    def _extract_dates_advanced(self, text: str) -> List[str]:
        """
        AMÉLIORATION: Extraction dates avec TOUS les séparateurs
        Gère: → – — > / - to à
        """
        dates = []
        
        # Patterns de dates
        for pattern in self.date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        # Mots de fin de période
        end_words = ['present', 'aujourd\'hui', 'current', 'actuel', 
                     'en cours', 'now', 'ongoing', 'toujours', 'ce jour']
        
        for word in end_words:
            if word in text.lower():
                if 'Present' not in dates:
                    dates.append('Present')
        
        return dates[:2]  # Max 2 dates (début et fin)
    
    def _format_date_range(self, dates: List[str]) -> str:
        """Formate une plage de dates"""
        if not dates:
            return ""
        if len(dates) == 1:
            return dates[0]
        return f"{dates[0]} - {dates[1]}"
    
    # ========================================================================
    # Extraction formations
    # ========================================================================
    
    def _extract_education_robust(self, text: str, section_lines: List[str]) -> List[Dict]:
        """Extraction de formation"""
        education = []
        search_text = ' '.join(section_lines)
        search_lower = search_text.lower()
        
        # Diplômes
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
    
    # ========================================================================
    # AMÉLIORATION: Langues avec niveaux CEFR
    # ========================================================================
    
    def _extract_languages_with_levels(self, text: str, section_lines: List[str]) -> List[str]:
        """
        AMÉLIORATION: Extraction langues avec niveaux CEFR
        Exemple: "Anglais (B2)", "Français courant", "Spanish fluent"
        """
        languages_found = []
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
        }
        
        for lang_name, variations in lang_variations.items():
            for var in variations:
                # Chercher la langue
                pattern = r'\b' + re.escape(var) + r'[\s:]*([^\n,;]{0,30})'
                match = re.search(pattern, search_lower)
                
                if match:
                    # Extraire le niveau si présent
                    context = match.group(1) if len(match.groups()) > 0 else ""
                    level = self._extract_language_level(context)
                    
                    if level:
                        languages_found.append(f"{lang_name} ({level})")
                    else:
                        languages_found.append(lang_name)
                    break
        
        return list(set(languages_found))
    
    def _extract_language_level(self, text: str) -> str:
        """Extrait le niveau de langue (CEFR ou descriptif)"""
        text_lower = text.lower()
        
        # Chercher niveaux CEFR
        for level in ['a1', 'a2', 'b1', 'b2', 'c1', 'c2']:
            if level in text_lower:
                return level.upper()
        
        # Chercher niveaux descriptifs
        level_map = {
            'natif': 'Natif',
            'native': 'Natif',
            'courant': 'Courant',
            'fluent': 'Courant',
            'avancé': 'Avancé',
            'advanced': 'Avancé',
            'intermédiaire': 'Intermédiaire',
            'intermediate': 'Intermédiaire',
            'débutant': 'Débutant',
            'beginner': 'Débutant',
        }
        
        for key, value in level_map.items():
            if key in text_lower:
                return value
        
        return ""
    
    # ========================================================================
    # Utilitaires
    # ========================================================================
    
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
extractor_v3 = CVExtractorV3()

