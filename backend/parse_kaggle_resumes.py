"""
Parser pour le dataset Kaggle UpdatedResumeDataSet.csv
Extrait toutes les compétences uniques des CV réels
"""
import pandas as pd
import json
import re
from pathlib import Path
from collections import Counter
from typing import Set, List, Dict

def extract_skills_from_text(text: str) -> Set[str]:
    """
    Extrait les compétences d'un texte de CV
    """
    skills = set()
    
    # Patterns pour détecter les compétences
    skill_patterns = [
        # Langages programmation
        r'\b(Python|JavaScript|Java|C\+\+|C#|PHP|Ruby|Go|Rust|Swift|Kotlin|Scala|R|TypeScript|Perl|Shell|Bash)\b',
        
        # Frameworks
        r'\b(React|Angular|Vue\.?js|Django|Flask|FastAPI|Spring|Express\.?js|Node\.?js|Laravel|Symfony|Rails|Next\.?js|Nuxt\.?js)\b',
        
        # Bases de données
        r'\b(SQL|MySQL|PostgreSQL|MongoDB|Redis|Oracle|SQLite|Cassandra|Elasticsearch|DynamoDB|Neo4j)\b',
        
        # DevOps & Cloud
        r'\b(Docker|Kubernetes|AWS|Azure|GCP|Google Cloud|Jenkins|GitLab|GitHub|Terraform|Ansible|Vagrant)\b',
        
        # Data & AI
        r'\b(Machine Learning|Deep Learning|NLP|TensorFlow|PyTorch|Keras|Scikit-learn|Pandas|NumPy|Spark|Hadoop|Kafka|Tableau|Power BI)\b',
        
        # Mobile
        r'\b(Android|iOS|React Native|Flutter|Xamarin)\b',
        
        # Web
        r'\b(HTML|CSS|SASS|LESS|Bootstrap|Tailwind|Webpack|API|REST|GraphQL)\b',
        
        # Outils
        r'\b(Git|GitHub|GitLab|JIRA|Confluence|Agile|Scrum|Kanban)\b',
        
        # Design
        r'\b(Figma|Adobe XD|Sketch|Photoshop|Illustrator|InDesign|UI/UX)\b',
        
        # Systèmes
        r'\b(Linux|Unix|Windows|macOS)\b',
        
        # Soft skills
        r'\b(Leadership|Communication|Teamwork|Problem Solving|Critical Thinking|Creativity|Time Management|Organization)\b',
    ]
    
    text_upper = text.upper()
    text_lower = text.lower()
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            # Capitaliser correctement
            skills.add(match.strip())
    
    return skills

def parse_kaggle_dataset(csv_path: Path) -> Dict:
    """
    Parse le dataset Kaggle UpdatedResumeDataSet.csv
    """
    print("=" * 70)
    print("📊 Parsing du Dataset Kaggle - UpdatedResumeDataSet.csv")
    print("=" * 70)
    print()
    
    if not csv_path.exists():
        print(f"❌ Fichier introuvable: {csv_path}")
        print()
        print("📥 Veuillez placer le fichier téléchargé dans:")
        print(f"   {csv_path}")
        return None
    
    print(f"📂 Lecture du fichier: {csv_path.name}")
    
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
    
    # Extraire les compétences
    all_skills = set()
    skill_counter = Counter()
    categories = set()
    
    # Colonnes possibles dans le dataset
    text_column = None
    category_column = None
    
    for col in df.columns:
        col_lower = col.lower()
        if 'resume' in col_lower or 'text' in col_lower or 'description' in col_lower:
            text_column = col
        if 'category' in col_lower or 'job' in col_lower or 'role' in col_lower:
            category_column = col
    
    if not text_column:
        print("❌ Colonne de texte de CV non trouvée")
        return None
    
    print(f"📝 Colonne texte: {text_column}")
    if category_column:
        print(f"📁 Colonne catégorie: {category_column}")
    print()
    
    print("🔍 Extraction des compétences...")
    
    for idx, row in df.iterrows():
        text = str(row[text_column])
        
        if category_column:
            category = str(row[category_column])
            categories.add(category)
        
        # Extraire compétences
        skills = extract_skills_from_text(text)
        all_skills.update(skills)
        
        for skill in skills:
            skill_counter[skill] += 1
        
        if (idx + 1) % 100 == 0:
            print(f"   Traité: {idx + 1}/{len(df)} CV...")
    
    print(f"\n✅ Extraction terminée!")
    print(f"   Total CV analysés: {len(df)}")
    print(f"   Compétences uniques: {len(all_skills)}")
    if categories:
        print(f"   Catégories: {len(categories)}")
    print()
    
    # Trier par fréquence
    most_common = skill_counter.most_common(50)
    
    print("🔝 Top 20 compétences les plus fréquentes:")
    for i, (skill, count) in enumerate(most_common[:20], 1):
        print(f"   {i:2d}. {skill:30s} - {count:4d} fois")
    
    return {
        'all_skills': all_skills,
        'skill_counter': skill_counter,
        'categories': categories,
        'total_cvs': len(df)
    }

def classify_skills(skills: Set[str]) -> Dict[str, List[str]]:
    """
    Classifie les compétences en technical vs soft skills
    """
    technical_keywords = {
        'python', 'java', 'javascript', 'sql', 'html', 'css', 'react',
        'angular', 'vue', 'django', 'flask', 'spring', 'node', 'docker',
        'kubernetes', 'aws', 'azure', 'git', 'api', 'database', 'linux',
        'android', 'ios', 'mongodb', 'mysql', 'postgresql', 'redis',
        'tensorflow', 'pytorch', 'machine learning', 'deep learning',
        'data', 'cloud', 'devops', 'framework', 'library', 'tool'
    }
    
    soft_keywords = {
        'leadership', 'communication', 'teamwork', 'management', 'problem',
        'critical', 'thinking', 'creativity', 'time', 'organization',
        'analytical', 'interpersonal', 'collaboration', 'negotiation'
    }
    
    technical = []
    soft = []
    
    for skill in skills:
        skill_lower = skill.lower()
        
        is_technical = any(kw in skill_lower for kw in technical_keywords)
        is_soft = any(kw in skill_lower for kw in soft_keywords)
        
        if is_technical:
            technical.append(skill)
        elif is_soft:
            soft.append(skill)
        else:
            # Par défaut, considérer comme technique
            technical.append(skill)
    
    return {
        'technical_skills': sorted(technical),
        'soft_skills': sorted(soft)
    }

def save_to_json(data: Dict, output_path: Path):
    """
    Sauvegarde les compétences en JSON
    """
    classified = classify_skills(data['all_skills'])
    
    output_data = {
        'technical_skills': classified['technical_skills'],
        'soft_skills': classified['soft_skills'],
        'metadata': {
            'total_skills': len(data['all_skills']),
            'technical': len(classified['technical_skills']),
            'soft': len(classified['soft_skills']),
            'source': 'Kaggle UpdatedResumeDataSet',
            'total_cvs_analyzed': data['total_cvs'],
            'categories': list(data['categories'])
        },
        'top_skills': [
            {'skill': skill, 'frequency': count}
            for skill, count in data['skill_counter'].most_common(100)
        ]
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Fichier créé: {output_path}")
    print(f"   Taille: {output_path.stat().st_size / 1024:.1f} KB")
    print(f"   - Compétences techniques: {len(classified['technical_skills'])}")
    print(f"   - Soft skills: {len(classified['soft_skills'])}")

def main():
    """Point d'entrée principal"""
    print()
    print("=" * 70)
    print("🎯 Kaggle Resume Dataset Parser")
    print("=" * 70)
    print()
    
    # Chemins
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    csv_path = data_dir / "UpdatedResumeDataSet.csv"
    output_path = data_dir / "kaggle_skills.json"
    
    # Parser le dataset
    result = parse_kaggle_dataset(csv_path)
    
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
    print("   1. Le fichier sera automatiquement détecté")
    print("   2. Ou fusionnez avec ESCO pour plus de compétences")

if __name__ == "__main__":
    main()

