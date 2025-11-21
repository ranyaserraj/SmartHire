"""
Traduit les compétences du fichier resume_skills_complete.json en français
Crée resume_skills_complete_fr.json
"""
import sys
import io
# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
from pathlib import Path
from typing import Dict, List, Set

# Dictionnaire de traduction EN → FR pour les compétences
TRANSLATIONS = {
    # Langages de programmation
    'Python': 'Python',
    'Java': 'Java',
    'JavaScript': 'JavaScript',
    'C++': 'C++',
    'C#': 'C#',
    'Php': 'PHP',
    'Ruby': 'Ruby',
    'Swift': 'Swift',
    'Kotlin': 'Kotlin',
    'Go': 'Go',
    'Rust': 'Rust',
    'Typescript': 'TypeScript',
    'Scala': 'Scala',
    'R': 'R',
    
    # Technologies & Frameworks
    'Machine Learning': 'Apprentissage Automatique',
    'Deep Learning': 'Apprentissage Profond',
    'Natural Language Processing': 'Traitement du Langage Naturel',
    'Artificial Intelligence': 'Intelligence Artificielle',
    'Data Science': 'Science des Données',
    'Data Analysis': 'Analyse de Données',
    'Data Analytics': 'Analytique de Données',
    'Data Mining': 'Exploration de Données',
    'Big Data': 'Big Data',
    'Cloud Computing': 'Informatique en Nuage',
    'Sql': 'SQL',
    'Mysql': 'MySQL',
    'Postgresql': 'PostgreSQL',
    'Mongodb': 'MongoDB',
    'Oracle': 'Oracle',
    'Database Management': 'Gestion de Bases de Données',
    'Excel': 'Excel',
    'Microsoft Office': 'Microsoft Office',
    'Word': 'Word',
    'Powerpoint': 'PowerPoint',
    'Access': 'Access',
    'Outlook': 'Outlook',
    'Power Bi': 'Power BI',
    'Tableau': 'Tableau',
    'Sap': 'SAP',
    
    # Web & Mobile
    'Html': 'HTML',
    'Css': 'CSS',
    'React': 'React',
    'Angular': 'Angular',
    'Vue.Js': 'Vue.js',
    'Node.Js': 'Node.js',
    'Django': 'Django',
    'Flask': 'Flask',
    'Spring': 'Spring',
    'Android': 'Android',
    'Ios': 'iOS',
    
    # DevOps & Cloud
    'Docker': 'Docker',
    'Kubernetes': 'Kubernetes',
    'Git': 'Git',
    'Jenkins': 'Jenkins',
    'Aws': 'AWS',
    'Azure': 'Azure',
    'Google Cloud': 'Google Cloud',
    
    # Business & Finance
    'Accounting': 'Comptabilité',
    'Financial': 'Financier',
    'Financial Analysis': 'Analyse Financière',
    'Budget': 'Budget',
    'Contracts': 'Contrats',
    'Inventory': 'Inventaire',
    'Sales': 'Ventes',
    'Marketing': 'Marketing',
    'Business Development': 'Développement Commercial',
    'Customer Service': 'Service Client',
    'Project Management': 'Gestion de Projet',
    'Team Management': 'Gestion d\'Équipe',
    'Quality': 'Qualité',
    'Processes': 'Processus',
    'Clients': 'Clients',
    'Documentation': 'Documentation',
    
    # Soft Skills
    'Communication': 'Communication',
    'Leadership': 'Leadership',
    'Teamwork': 'Travail d\'Équipe',
    'Problem Solving': 'Résolution de Problèmes',
    'Critical Thinking': 'Pensée Critique',
    'Creativity': 'Créativité',
    'Time Management': 'Gestion du Temps',
    'Organization': 'Organisation',
    'Organizational Skills': 'Compétences Organisationnelles',
    'Adaptability': 'Adaptabilité',
    'Flexibility': 'Flexibilité',
    'Attention To Detail': 'Souci du Détail',
    'Decision Making': 'Prise de Décision',
    'Conflict Resolution': 'Résolution de Conflits',
    'Negotiation': 'Négociation',
    'Planning': 'Planification',
    'Strategic Thinking': 'Pensée Stratégique',
    'Analytical Skills': 'Compétences Analytiques',
    'Interpersonal Skills': 'Compétences Interpersonnelles',
    'Collaboration': 'Collaboration',
    'Presentation Skills': 'Compétences de Présentation',
    'Public Speaking': 'Prise de Parole en Public',
    'Writing': 'Rédaction',
    'Research': 'Recherche',
    
    # Autres domaines techniques
    'Tensorflow': 'TensorFlow',
    'Pytorch': 'PyTorch',
    'Keras': 'Keras',
    'Scikit-Learn': 'Scikit-Learn',
    'Pandas': 'Pandas',
    'Numpy': 'NumPy',
    'Hadoop': 'Hadoop',
    'Spark': 'Spark',
    'Kafka': 'Kafka',
    'Api': 'API',
    'Rest': 'REST',
    'Graphql': 'GraphQL',
    'Microservices': 'Microservices',
    'Agile': 'Agile',
    'Scrum': 'Scrum',
    'Devops': 'DevOps',
    'Testing': 'Tests',
    'Ci/Cd': 'CI/CD',
    'Networking': 'Réseaux',
    'Security': 'Sécurité',
    'Cybersecurity': 'Cybersécurité',
    'Blockchain': 'Blockchain',
    'Iot': 'IoT',
}

def translate_skill(skill: str) -> str:
    """
    Traduit une compétence en français
    """
    # Vérifier si traduction directe existe
    if skill in TRANSLATIONS:
        return TRANSLATIONS[skill]
    
    # Vérifier en minuscules
    skill_lower = skill.lower()
    for en, fr in TRANSLATIONS.items():
        if en.lower() == skill_lower:
            return fr
    
    # Règles de traduction automatique pour termes courants
    skill_translated = skill
    
    # Remplacements courants
    replacements = {
        'Management': 'Gestion',
        'Manager': 'Gestionnaire',
        'Development': 'Développement',
        'Developer': 'Développeur',
        'Engineering': 'Ingénierie',
        'Engineer': 'Ingénieur',
        'Analysis': 'Analyse',
        'Analyst': 'Analyste',
        'Design': 'Conception',
        'Designer': 'Concepteur',
        'Administration': 'Administration',
        'Administrator': 'Administrateur',
        'Consulting': 'Conseil',
        'Consultant': 'Consultant',
        'Strategy': 'Stratégie',
        'Strategic': 'Stratégique',
        'Operations': 'Opérations',
        'Operational': 'Opérationnel',
        'Technical': 'Technique',
        'Technology': 'Technologie',
        'Software': 'Logiciel',
        'Hardware': 'Matériel',
        'Network': 'Réseau',
        'System': 'Système',
        'Programming': 'Programmation',
        'Coding': 'Codage',
        'Testing': 'Tests',
        'Quality Assurance': 'Assurance Qualité',
    }
    
    for en, fr in replacements.items():
        if en in skill:
            skill_translated = skill.replace(en, fr)
            break
    
    # Si aucune traduction trouvée, garder l'original
    return skill_translated

def translate_skills_file(input_path: Path, output_path: Path):
    """
    Traduit le fichier de compétences en français
    """
    print("=" * 70)
    print("🇫🇷 Traduction des Compétences en Français")
    print("=" * 70)
    print()
    
    if not input_path.exists():
        print(f"❌ Fichier introuvable: {input_path}")
        return
    
    print(f"📂 Lecture: {input_path.name}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"   Compétences techniques: {len(data['technical_skills'])}")
    print(f"   Soft skills: {len(data['soft_skills'])}")
    print()
    
    print("🔄 Traduction en cours...")
    
    # Traduire les compétences
    technical_translated = []
    soft_translated = []
    
    translations_made = 0
    kept_original = 0
    
    for skill in data['technical_skills']:
        translated = translate_skill(skill)
        technical_translated.append(translated)
        if translated != skill:
            translations_made += 1
        else:
            kept_original += 1
    
    for skill in data['soft_skills']:
        translated = translate_skill(skill)
        soft_translated.append(translated)
        if translated != skill:
            translations_made += 1
        else:
            kept_original += 1
    
    # Créer le nouveau fichier
    translated_data = {
        'technical_skills': sorted(list(set(technical_translated))),  # Dédupliquer
        'soft_skills': sorted(list(set(soft_translated))),
        'metadata': {
            'total_skills': len(set(technical_translated)) + len(set(soft_translated)),
            'technical': len(set(technical_translated)),
            'soft': len(set(soft_translated)),
            'source': data['metadata']['source'] + ' - Traduit en français',
            'total_cvs_analyzed': data['metadata']['total_cvs_analyzed'],
            'language': 'français',
            'translations_made': translations_made,
            'kept_original': kept_original
        }
    }
    
    # Si le fichier original a des top_skills, les traduire aussi
    if 'top_skills' in data:
        translated_data['top_skills'] = [
            {
                'skill': translate_skill(item['skill']),
                'skill_original': item['skill'],
                'frequency': item['frequency'],
                'type': item['type']
            }
            for item in data['top_skills'][:200]  # Top 200
        ]
    
    # Sauvegarder
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Traduction terminée!")
    print(f"   Traductions effectuées: {translations_made}")
    print(f"   Conservées (termes techniques): {kept_original}")
    print(f"   Total après déduplication: {translated_data['metadata']['total_skills']}")
    print()
    
    print(f"💾 Fichier créé: {output_path}")
    print(f"   Taille: {output_path.stat().st_size / 1024:.1f} KB")
    
    # Afficher quelques exemples
    print("\n📋 Exemples de traductions:")
    examples = [
        ('Machine Learning', 'Apprentissage Automatique'),
        ('Data Analysis', 'Analyse de Données'),
        ('Project Management', 'Gestion de Projet'),
        ('Communication', 'Communication'),
        ('Python', 'Python'),
    ]
    for en, fr in examples:
        if en in data['technical_skills'] or en in data['soft_skills']:
            print(f"   • {en:30s} → {fr}")

def main():
    """Point d'entrée principal"""
    print()
    print("=" * 70)
    print("🎯 Traducteur de Compétences EN → FR")
    print("=" * 70)
    print()
    
    data_dir = Path(__file__).parent / "data"
    
    input_path = data_dir / "resume_skills_complete.json"
    output_path = data_dir / "resume_skills_complete_fr.json"
    
    translate_skills_file(input_path, output_path)
    
    print()
    print("=" * 70)
    print("✅ Terminé!")
    print("=" * 70)
    print()
    print("📂 Fichier créé:")
    print(f"   {output_path}")
    print()
    print("🔧 Le fichier sera automatiquement utilisé par esco_loader.py")
    print("   (priorité donnée aux compétences françaises)")

if __name__ == "__main__":
    main()

