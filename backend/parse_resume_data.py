"""
Parser pour le dataset Kaggle resume_data.csv
Extrait toutes les compétences de la colonne 'skills' - Tous domaines
"""
import sys
import io
# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pandas as pd
import json
import ast
from pathlib import Path
from collections import Counter
from typing import Set, List, Dict

def parse_skills_column(skills_str: str) -> List[str]:
    """
    Parse la colonne skills qui est au format:
    ['Big Data', 'Hadoop', 'Hive', 'Python', ...]
    """
    if pd.isna(skills_str) or not skills_str:
        return []
    
    try:
        # Si c'est déjà une liste Python (format string)
        if skills_str.startswith('[') and skills_str.endswith(']'):
            # Utiliser ast.literal_eval pour parser de manière sécurisée
            skills_list = ast.literal_eval(skills_str)
            if isinstance(skills_list, list):
                return [str(skill).strip() for skill in skills_list if skill]
        
        # Si c'est séparé par des virgules
        if ',' in skills_str:
            return [s.strip() for s in skills_str.split(',') if s.strip()]
        
        # Sinon, retourner comme une seule compétence
        return [skills_str.strip()] if skills_str.strip() else []
    
    except Exception as e:
        print(f"⚠️ Erreur parsing: {skills_str[:50]}... - {e}")
        return []

def classify_skill(skill: str) -> str:
    """
    Classifie une compétence en technical ou soft skill
    """
    soft_keywords = {
        'communication', 'leadership', 'teamwork', 'management', 'problem',
        'critical', 'thinking', 'creativity', 'time', 'organization',
        'analytical', 'interpersonal', 'collaboration', 'negotiation',
        'presentation', 'planning', 'decision', 'conflict', 'motivation',
        'adaptability', 'flexibility', 'initiative', 'attention to detail',
        'work ethic', 'customer service', 'sales', 'marketing', 'business',
        'strategic', 'project management', 'team management', 'coaching',
        'mentoring', 'networking', 'public speaking', 'writing', 'research'
    }
    
    skill_lower = skill.lower()
    
    # Vérifier si c'est un soft skill
    for keyword in soft_keywords:
        if keyword in skill_lower:
            return 'soft'
    
    # Sinon, c'est une compétence technique
    return 'technical'

def parse_resume_data_csv(csv_path: Path) -> Dict:
    """
    Parse le dataset resume_data.csv avec colonne skills
    """
    print("=" * 70)
    print("📊 Parsing du Dataset Kaggle - resume_data.csv")
    print("=" * 70)
    print()
    
    if not csv_path.exists():
        print(f"❌ Fichier introuvable: {csv_path}")
        print()
        print("📥 Veuillez placer le fichier dans:")
        print(f"   {csv_path}")
        return None
    
    print(f"📂 Lecture du fichier: {csv_path.name}")
    print(f"   Taille: {csv_path.stat().st_size / (1024*1024):.1f} MB")
    
    # Lire le CSV avec différents encodages
    df = None
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            print(f"   Essai encodage: {encoding}...")
            df = pd.read_csv(csv_path, encoding=encoding)
            print(f"   ✅ Succès avec {encoding}")
            break
        except Exception as e:
            print(f"   ❌ Échec: {e}")
            continue
    
    if df is None:
        print("❌ Impossible de lire le fichier")
        return None
    
    print(f"\n📊 Dataset chargé:")
    print(f"   Lignes: {len(df)}")
    print(f"   Colonnes: {list(df.columns)}")
    print()
    
    # Vérifier la colonne skills
    if 'skills' not in df.columns and 'Skills' not in df.columns:
        print("❌ Colonne 'skills' non trouvée")
        print(f"   Colonnes disponibles: {list(df.columns)}")
        return None
    
    # Trouver le nom exact de la colonne skills
    skills_col = 'skills' if 'skills' in df.columns else 'Skills'
    print(f"📝 Colonne skills: {skills_col}")
    print()
    
    # Extraire toutes les compétences
    all_skills = set()
    skill_counter = Counter()
    technical_skills = set()
    soft_skills = set()
    
    print("🔍 Extraction des compétences...")
    
    total_rows = len(df)
    errors = 0
    
    for idx, row in df.iterrows():
        try:
            skills_str = row[skills_col]
            skills_list = parse_skills_column(skills_str)
            
            for skill in skills_list:
                # Nettoyer la compétence
                skill_clean = skill.strip()
                
                if not skill_clean or len(skill_clean) < 2:
                    continue
                
                # Normaliser (capitaliser)
                skill_normalized = skill_clean.title()
                
                all_skills.add(skill_normalized)
                skill_counter[skill_normalized] += 1
                
                # Classifier
                if classify_skill(skill_normalized) == 'soft':
                    soft_skills.add(skill_normalized)
                else:
                    technical_skills.add(skill_normalized)
            
            if (idx + 1) % 100 == 0:
                print(f"   Traité: {idx + 1}/{total_rows} CV...")
        
        except Exception as e:
            errors += 1
            if errors < 5:  # Afficher seulement les 5 premières erreurs
                print(f"   ⚠️ Erreur ligne {idx}: {e}")
            continue
    
    print(f"\n✅ Extraction terminée!")
    print(f"   Total CV analysés: {total_rows}")
    print(f"   Compétences uniques: {len(all_skills)}")
    print(f"   - Techniques: {len(technical_skills)}")
    print(f"   - Soft skills: {len(soft_skills)}")
    print(f"   Erreurs ignorées: {errors}")
    print()
    
    # Afficher le top 30
    most_common = skill_counter.most_common(30)
    
    print("🔝 Top 30 compétences les plus fréquentes:")
    for i, (skill, count) in enumerate(most_common, 1):
        skill_type = "📘" if skill in technical_skills else "🌟"
        print(f"   {i:2d}. {skill_type} {skill:40s} - {count:5d} fois")
    
    return {
        'all_skills': all_skills,
        'technical_skills': technical_skills,
        'soft_skills': soft_skills,
        'skill_counter': skill_counter,
        'total_cvs': total_rows
    }

def save_to_json(data: Dict, output_path: Path):
    """
    Sauvegarde les compétences en JSON
    """
    output_data = {
        'technical_skills': sorted(list(data['technical_skills'])),
        'soft_skills': sorted(list(data['soft_skills'])),
        'metadata': {
            'total_skills': len(data['all_skills']),
            'technical': len(data['technical_skills']),
            'soft': len(data['soft_skills']),
            'source': 'Kaggle resume_data.csv (Multi-domaines)',
            'total_cvs_analyzed': data['total_cvs']
        },
        'top_skills': [
            {
                'skill': skill,
                'frequency': count,
                'type': 'soft' if skill in data['soft_skills'] else 'technical'
            }
            for skill, count in data['skill_counter'].most_common(200)
        ]
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Fichier créé: {output_path}")
    print(f"   Taille: {output_path.stat().st_size / 1024:.1f} KB")
    print(f"   - Compétences techniques: {len(data['technical_skills'])}")
    print(f"   - Soft skills: {len(data['soft_skills'])}")

def main():
    """Point d'entrée principal"""
    print()
    print("=" * 70)
    print("🎯 Resume Data Parser - Multi-domaines")
    print("=" * 70)
    print()
    
    # Chemins
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    csv_path = data_dir / "resume_data.csv"
    output_path = data_dir / "resume_skills_complete.json"
    
    # Parser le dataset
    result = parse_resume_data_csv(csv_path)
    
    if not result:
        return
    
    # Sauvegarder
    save_to_json(result, output_path)
    
    print()
    print("=" * 70)
    print("✅ Terminé!")
    print("=" * 70)
    print()
    print("📂 Fichier créé:")
    print(f"   {output_path}")
    print()
    print("🔧 Pour utiliser avec la V3:")
    print("   Le fichier sera automatiquement détecté par esco_loader.py")
    print()
    print("🚀 Redémarrez le serveur:")
    print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080")

if __name__ == "__main__":
    main()

