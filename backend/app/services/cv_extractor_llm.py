"""
Service d'extraction de CV avec LLM (OpenAI GPT-4 ou Claude)
Pour atteindre 95-98% de précision

USAGE:
1. Installer : pip install openai
2. Définir : OPENAI_API_KEY dans .env
3. Remplacer dans cvs.py : CVExtractorV2 → CVExtractorLLM
"""
import os
import json
import re
from typing import Dict, List, Optional
from pathlib import Path
from .cv_extractor_v2 import CVExtractorV2


class CVExtractorLLM:
    """Extracteur de CV avec IA (OpenAI GPT-4)"""
    
    def __init__(self):
        self.v2_extractor = CVExtractorV2()  # Fallback
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.use_llm = bool(self.api_key)
        
        if not self.use_llm:
            print("⚠️ OPENAI_API_KEY non définie, utilisation du CV Extractor V2")
    
    def extract_from_file(self, file_path: str) -> Dict:
        """Point d'entrée principal"""
        # Étape 1: Extraire le texte brut avec V2
        v2_result = self.v2_extractor.extract_from_file(file_path)
        
        # Si pas d'API key, retourner résultat V2
        if not self.use_llm:
            return v2_result
        
        # Étape 2: Améliorer avec LLM
        try:
            # Extraire le texte brut pour le LLM
            text = self._extract_raw_text(file_path)
            
            if len(text) < 100:
                return v2_result
            
            # Envoyer au LLM
            llm_result = self._extract_with_llm(text)
            
            # Merger les résultats (LLM prioritaire, V2 en fallback)
            return self._merge_results(llm_result, v2_result)
        
        except Exception as e:
            print(f"LLM extraction failed: {e}, falling back to V2")
            return v2_result
    
    def _extract_raw_text(self, file_path: str) -> str:
        """Extrait le texte brut du fichier"""
        import pdfplumber
        from PIL import Image
        import pytesseract
        
        file_path = Path(file_path)
        text = ""
        
        if file_path.suffix.lower() == '.pdf':
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                print(f"PDF extraction failed: {e}")
        
        elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            try:
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image, lang='fra+eng')
            except Exception as e:
                print(f"Image OCR failed: {e}")
        
        return text
    
    def _extract_with_llm(self, text: str) -> Dict:
        """Extrait les données avec GPT-4"""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("pip install openai required for LLM extraction")
        
        client = OpenAI(api_key=self.api_key)
        
        # Limiter le texte à 4000 caractères pour économiser les tokens
        text_truncated = text[:4000]
        
        prompt = f"""Tu es un expert en analyse de CV. Extrait les informations suivantes du CV ci-dessous.

Réponds UNIQUEMENT avec un objet JSON valide contenant ces champs :
{{
  "nom": "Nom complet du candidat",
  "email": "Adresse email",
  "telephone": "Numéro de téléphone",
  "ville": "Ville de résidence",
  "competences_extraites": ["liste", "de", "compétences", "techniques"],
  "experience": [
    {{
      "poste": "Intitulé du poste",
      "entreprise": "Nom de l'entreprise",
      "periode": "Dates (ex: Jan 2020 - Present)",
      "missions": ["Mission 1", "Mission 2"]
    }}
  ],
  "formation": [
    {{
      "diplome": "Nom du diplôme",
      "etablissement": "Nom de l'école/université",
      "annee": "Année d'obtention"
    }}
  ],
  "langues": ["Français", "Anglais"]
}}

Règles importantes :
1. Si une information est absente, utilise une chaîne vide "" ou liste vide []
2. Pour les compétences, extrais TOUTES les technologies, langages, frameworks mentionnés
3. Pour les dates, standardise au format "Mois Année - Mois Année" ou "Mois Année - Present"
4. Sépare chaque expérience professionnelle
5. Réponds UNIQUEMENT avec le JSON, pas de texte avant/après

CV:
{text_truncated}
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Plus économique que gpt-4
                messages=[
                    {"role": "system", "content": "Tu es un expert en analyse de CV. Tu réponds uniquement en JSON valide."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Plus déterministe
                max_tokens=1500
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Nettoyer le texte (supprimer markdown si présent)
            result_text = re.sub(r'^```json\s*', '', result_text)
            result_text = re.sub(r'\s*```$', '', result_text)
            
            # Parser le JSON
            result = json.loads(result_text)
            
            return result
        
        except json.JSONDecodeError as e:
            print(f"LLM returned invalid JSON: {e}")
            raise
        except Exception as e:
            print(f"LLM API error: {e}")
            raise
    
    def _merge_results(self, llm_result: Dict, v2_result: Dict) -> Dict:
        """Merge les résultats LLM et V2 (LLM prioritaire)"""
        merged = {}
        
        # Pour chaque champ, préférer LLM si non vide
        fields = ["nom", "email", "telephone", "ville"]
        for field in fields:
            llm_value = llm_result.get(field, "")
            v2_value = v2_result.get(field, "")
            merged[field] = llm_value if llm_value else v2_value
        
        # Compétences : union des deux
        llm_skills = set(llm_result.get("competences_extraites", []))
        v2_skills = set(v2_result.get("competences_extraites", []))
        merged["competences_extraites"] = sorted(list(llm_skills | v2_skills))
        
        # Expériences : préférer LLM (plus structurées)
        merged["experience"] = llm_result.get("experience", []) or v2_result.get("experience", [])
        
        # Formation : préférer LLM
        merged["formation"] = llm_result.get("formation", []) or v2_result.get("formation", [])
        
        # Langues : union
        llm_langs = set(llm_result.get("langues", []))
        v2_langs = set(v2_result.get("langues", []))
        merged["langues"] = sorted(list(llm_langs | v2_langs))
        
        return merged


# Instance globale
extractor_llm = CVExtractorLLM()

