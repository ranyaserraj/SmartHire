"""
Module pour charger et interroger le référentiel ESCO
ESCO = European Skills, Competences, Qualifications and Occupations
"""
import json
import csv
from pathlib import Path
from typing import List, Dict, Set, Optional
from rapidfuzz import fuzz, process
import re


class ESCOLoader:
    """
    Charge et interroge le référentiel ESCO des compétences
    
    Dataset ESCO officiel : 13 000+ compétences en 28 langues
    Source : https://esco.ec.europa.eu/en/use-esco/download
    """
    
    def __init__(self):
        self.skills_data = None
        self.technical_skills = set()
        self.soft_skills = set()
        self.all_skills = set()
        self.skills_by_language = {}
        
        # Charger les compétences
        self._load_esco_data()
    
    def _load_esco_data(self):
        """Charge les données ESCO depuis le fichier local"""
        # Chemin vers les données
        data_dir = Path(__file__).parent.parent.parent / "data"
        
        # Ordre de priorité des datasets
        kaggle_dataset = data_dir / "kaggle_skills.json"
        esco_complete = data_dir / "esco_skills_complete.json"
        esco_extended = data_dir / "esco_skills_extended.json"
        esco_full_csv = data_dir / "esco_skills_full.csv"
        esco_full_json = data_dir / "esco_skills_full.json"
        esco_sample = data_dir / "esco_skills_sample.json"
        
        # 1. Priorité: Dataset Kaggle (CV réels)
        if kaggle_dataset.exists():
            print("🎯 Chargement du dataset Kaggle (CV réels)...")
            self._load_from_json(kaggle_dataset)
        
        # 2. Dataset ESCO complet fusionné
        elif esco_complete.exists():
            print("📚 Chargement du dataset ESCO complet...")
            self._load_from_json(esco_complete)
        
        # 3. Dataset étendu avec compétences populaires
        elif esco_extended.exists():
            print("📚 Chargement du dataset étendu...")
            self._load_from_json(esco_extended)
        
        # 4. CSV ESCO officiel
        elif esco_full_csv.exists():
            print("📚 Chargement du CSV ESCO...")
            self._load_from_csv(esco_full_csv)
        
        # 5. JSON ESCO parsé
        elif esco_full_json.exists():
            print("📚 Chargement du JSON ESCO...")
            self._load_from_json(esco_full_json)
        
        # 6. Échantillon (fallback)
        elif esco_sample.exists():
            print("⚠️ Utilisation du dataset d'échantillon (limité à 139 compétences)")
            print("   📥 Pour améliorer:")
            print("   Option 1: Kaggle UpdatedResumeDataSet.csv")
            print("      → Placez dans: backend/data/UpdatedResumeDataSet.csv")
            print("      → Exécutez: python parse_kaggle_resumes.py")
            print("   Option 2: ESCO complet")
            print("      → Téléchargez: https://esco.ec.europa.eu/en/use-esco/download")
            self._load_from_json(esco_sample)
        
        # 7. Aucun dataset trouvé
        else:
            print("❌ Aucun dataset trouvé")
            print("   📥 Options:")
            print("   1. Dataset Kaggle (recommandé)")
            print("   2. Dataset ESCO officiel")
            print("   3. Exécuter: python download_esco_complete.py")
            self._load_default_skills()
    
    def _load_from_csv(self, csv_path: Path):
        """Charge les compétences depuis le CSV ESCO complet"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                
                for row in reader:
                    # Structure du CSV ESCO :
                    # conceptUri, preferredLabel, altLabels, skillType, ...
                    
                    skill_name = row.get('preferredLabel', '').strip()
                    skill_type = row.get('skillType', '').lower()
                    language = row.get('language', 'en').lower()
                    
                    if not skill_name:
                        continue
                    
                    # Ajouter la compétence
                    self.all_skills.add(skill_name)
                    
                    # Classifier selon le type
                    if 'soft' in skill_type or 'transversal' in skill_type:
                        self.soft_skills.add(skill_name)
                    else:
                        self.technical_skills.add(skill_name)
                    
                    # Indexer par langue
                    if language not in self.skills_by_language:
                        self.skills_by_language[language] = set()
                    self.skills_by_language[language].add(skill_name)
                    
                    count += 1
                
                print(f"✅ {count} compétences ESCO chargées")
                print(f"   - Techniques: {len(self.technical_skills)}")
                print(f"   - Soft skills: {len(self.soft_skills)}")
                print(f"   - Langues: {len(self.skills_by_language)}")
        
        except Exception as e:
            print(f"❌ Erreur lors du chargement CSV ESCO: {e}")
            self._load_default_skills()
    
    def _load_from_json(self, json_path: Path):
        """Charge les compétences depuis le JSON d'échantillon"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.technical_skills = set(data.get('technical_skills', []))
            self.soft_skills = set(data.get('soft_skills', []))
            self.all_skills = self.technical_skills | self.soft_skills
            
            print(f"✅ {len(self.all_skills)} compétences chargées (échantillon)")
            print(f"   - Techniques: {len(self.technical_skills)}")
            print(f"   - Soft skills: {len(self.soft_skills)}")
        
        except Exception as e:
            print(f"❌ Erreur lors du chargement JSON: {e}")
            self._load_default_skills()
    
    def _load_default_skills(self):
        """Charge une liste minimale de compétences par défaut"""
        self.technical_skills = {
            'Python', 'JavaScript', 'Java', 'C++', 'React', 'Angular',
            'Django', 'Flask', 'SQL', 'PostgreSQL', 'MongoDB', 'Docker',
            'Kubernetes', 'AWS', 'Azure', 'Git', 'Linux', 'API', 'REST'
        }
        self.soft_skills = {
            'Leadership', 'Communication', 'Teamwork', 'Problem Solving',
            'Critical Thinking', 'Creativity', 'Time Management'
        }
        self.all_skills = self.technical_skills | self.soft_skills
        print(f"⚠️ Utilisation de la liste par défaut ({len(self.all_skills)} compétences)")
    
    def search_skills(self, text: str, threshold: int = 85) -> Dict[str, List[str]]:
        """
        Recherche les compétences dans un texte
        
        Args:
            text: Texte à analyser
            threshold: Seuil de similarité pour fuzzy matching (0-100)
        
        Returns:
            Dict avec 'technical' et 'soft' skills trouvées
        """
        text_lower = text.lower()
        found_skills = {
            'technical': set(),
            'soft': set()
        }
        
        # 1. Recherche exacte (rapide)
        for skill in self.technical_skills:
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
                found_skills['technical'].add(skill)
        
        for skill in self.soft_skills:
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
                found_skills['soft'].add(skill)
        
        # 2. Fuzzy matching (pour variations/typos)
        words = text.split()
        
        # Technical skills fuzzy
        for skill in self.technical_skills:
            if skill in found_skills['technical']:
                continue  # Déjà trouvé
            
            matches = process.extract(skill, words, scorer=fuzz.ratio, limit=1)
            if matches and matches[0][1] >= threshold:
                found_skills['technical'].add(skill)
        
        # Soft skills fuzzy
        for skill in self.soft_skills:
            if skill in found_skills['soft']:
                continue
            
            matches = process.extract(skill, words, scorer=fuzz.ratio, limit=1)
            if matches and matches[0][1] >= threshold:
                found_skills['soft'].add(skill)
        
        return {
            'technical': sorted(list(found_skills['technical'])),
            'soft': sorted(list(found_skills['soft']))
        }
    
    def get_skill_variations(self, skill: str) -> List[str]:
        """Retourne les variations d'une compétence (synonymes, traductions)"""
        # TODO: Implémenter avec les altLabels du CSV ESCO
        return [skill]
    
    def is_technical_skill(self, skill: str) -> bool:
        """Vérifie si une compétence est technique"""
        return skill in self.technical_skills
    
    def is_soft_skill(self, skill: str) -> bool:
        """Vérifie si une compétence est une soft skill"""
        return skill in self.soft_skills
    
    def get_all_skills(self, language: Optional[str] = None) -> List[str]:
        """Retourne toutes les compétences, optionnellement filtrées par langue"""
        if language and language in self.skills_by_language:
            return sorted(list(self.skills_by_language[language]))
        return sorted(list(self.all_skills))
    
    def get_stats(self) -> Dict:
        """Retourne les statistiques du dataset ESCO chargé"""
        return {
            'total_skills': len(self.all_skills),
            'technical_skills': len(self.technical_skills),
            'soft_skills': len(self.soft_skills),
            'languages': list(self.skills_by_language.keys()),
            'languages_count': len(self.skills_by_language)
        }


# Instance globale (singleton)
_esco_loader = None

def get_esco_loader() -> ESCOLoader:
    """Retourne l'instance globale du loader ESCO (singleton)"""
    global _esco_loader
    if _esco_loader is None:
        _esco_loader = ESCOLoader()
    return _esco_loader

