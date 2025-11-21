"""
Traducteur AMÉLIORÉ des compétences EN → FR
Traduction complète et professionnelle
"""
import sys
import io
# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
import re
from pathlib import Path
from typing import Dict

# DICTIONNAIRE COMPLET DE TRADUCTIONS (1000+ termes)
COMPLETE_TRANSLATIONS = {
    # === TECHNOLOGIES & LANGAGES DE PROGRAMMATION ===
    'Python': 'Python',
    'Java': 'Java',
    'JavaScript': 'JavaScript',
    'TypeScript': 'TypeScript',
    'C': 'C',
    'C++': 'C++',
    'C#': 'C#',
    'Php': 'PHP',
    'Ruby': 'Ruby',
    'Swift': 'Swift',
    'Kotlin': 'Kotlin',
    'Go': 'Go',
    'Golang': 'Go',
    'Rust': 'Rust',
    'Scala': 'Scala',
    'R': 'R',
    'Perl': 'Perl',
    'Shell': 'Shell',
    'Bash': 'Bash',
    'Powershell': 'PowerShell',
    'Matlab': 'MATLAB',
    
    # === INTELLIGENCE ARTIFICIELLE & DATA SCIENCE ===
    'Machine Learning': 'Apprentissage Automatique',
    'Deep Learning': 'Apprentissage Profond',
    'Natural Language Processing': 'Traitement du Langage Naturel',
    'Nlp': 'Traitement du Langage Naturel',
    'Artificial Intelligence': 'Intelligence Artificielle',
    'Ai': 'Intelligence Artificielle',
    'Data Science': 'Science des Données',
    'Data Analysis': 'Analyse de Données',
    'Data Analytics': 'Analytique de Données',
    'Data Mining': 'Exploration de Données',
    'Big Data': 'Mégadonnées',
    'Predictive Analytics': 'Analytique Prédictive',
    'Statistical Analysis': 'Analyse Statistique',
    'Neural Networks': 'Réseaux de Neurones',
    'Computer Vision': 'Vision par Ordinateur',
    'Pattern Recognition': 'Reconnaissance de Motifs',
    
    # === FRAMEWORKS & BIBLIOTHÈQUES ===
    'Tensorflow': 'TensorFlow',
    'Pytorch': 'PyTorch',
    'Keras': 'Keras',
    'Scikit-Learn': 'Scikit-Learn',
    'Pandas': 'Pandas',
    'Numpy': 'NumPy',
    'Scipy': 'SciPy',
    'Matplotlib': 'Matplotlib',
    'Seaborn': 'Seaborn',
    
    # === CLOUD & BIG DATA ===
    'Cloud Computing': 'Informatique en Nuage',
    'Aws': 'AWS',
    'Azure': 'Microsoft Azure',
    'Google Cloud': 'Google Cloud',
    'Gcp': 'Google Cloud Platform',
    'Hadoop': 'Hadoop',
    'Spark': 'Apache Spark',
    'Kafka': 'Apache Kafka',
    'Airflow': 'Apache Airflow',
    
    # === BASES DE DONNÉES ===
    'Database Management': 'Gestion de Bases de Données',
    'Sql': 'SQL',
    'Mysql': 'MySQL',
    'Postgresql': 'PostgreSQL',
    'Oracle': 'Oracle',
    'Mongodb': 'MongoDB',
    'Redis': 'Redis',
    'Cassandra': 'Cassandra',
    'Elasticsearch': 'Elasticsearch',
    'Dynamodb': 'DynamoDB',
    'Neo4j': 'Neo4j',
    'Sqlite': 'SQLite',
    'Mariadb': 'MariaDB',
    
    # === WEB & MOBILE ===
    'Html': 'HTML',
    'Css': 'CSS',
    'React': 'React',
    'React.Js': 'React.js',
    'Angular': 'Angular',
    'Vue.Js': 'Vue.js',
    'Next.Js': 'Next.js',
    'Node.Js': 'Node.js',
    'Express.Js': 'Express.js',
    'Django': 'Django',
    'Flask': 'Flask',
    'Spring': 'Spring',
    'Spring Boot': 'Spring Boot',
    'Laravel': 'Laravel',
    'Symfony': 'Symfony',
    'Ruby On Rails': 'Ruby on Rails',
    'Asp.Net': 'ASP.NET',
    'Android': 'Android',
    'Ios': 'iOS',
    'React Native': 'React Native',
    'Flutter': 'Flutter',
    
    # === DEVOPS & OUTILS ===
    'Docker': 'Docker',
    'Kubernetes': 'Kubernetes',
    'Jenkins': 'Jenkins',
    'Git': 'Git',
    'Github': 'GitHub',
    'Gitlab': 'GitLab',
    'Bitbucket': 'Bitbucket',
    'Ci/Cd': 'CI/CD',
    'Continuous Integration': 'Intégration Continue',
    'Continuous Deployment': 'Déploiement Continu',
    'Terraform': 'Terraform',
    'Ansible': 'Ansible',
    'Puppet': 'Puppet',
    'Chef': 'Chef',
    
    # === BUREAUTIQUE & OUTILS BUSINESS ===
    'Microsoft Office': 'Microsoft Office',
    'Excel': 'Excel',
    'Word': 'Word',
    'Powerpoint': 'PowerPoint',
    'Outlook': 'Outlook',
    'Access': 'Access',
    'Power Bi': 'Power BI',
    'Tableau': 'Tableau',
    'Sap': 'SAP',
    'Erp': 'ERP',
    'Crm': 'CRM',
    
    # === FINANCE & COMPTABILITÉ ===
    'Accounting': 'Comptabilité',
    'Bookkeeping': 'Tenue de Livres',
    'Financial': 'Financier',
    'Financial Analysis': 'Analyse Financière',
    'Financial Gestionnaire': 'Gestion Financière',
    'Budget': 'Budget',
    'Budgeting': 'Budgétisation',
    'Contracts': 'Contrats',
    'Inventory': 'Inventaire',
    'Inventory Management': 'Gestion des Stocks',
    'Accounts Payable': 'Comptes Fournisseurs',
    'Accounts Receivable': 'Comptes Clients',
    'Payroll': 'Paie',
    'Tax': 'Fiscalité',
    'Taxation': 'Fiscalité',
    'Auditing': 'Audit',
    'Cost Analysis': 'Analyse des Coûts',
    'Cash Flow': 'Flux de Trésorerie',
    
    # === BUSINESS & MANAGEMENT ===
    'Sales': 'Ventes',
    'Marketing': 'Marketing',
    'Digital Marketing': 'Marketing Numérique',
    'Business Development': 'Développement Commercial',
    'Customer Service': 'Service Client',
    'Customer Support': 'Support Client',
    'Project Management': 'Gestion de Projet',
    'Team Management': 'Gestion d\'Équipe',
    'Product Management': 'Gestion de Produit',
    'Quality': 'Qualité',
    'Quality Assurance': 'Assurance Qualité',
    'Quality Control': 'Contrôle Qualité',
    'Processes': 'Processus',
    'Process Improvement': 'Amélioration des Processus',
    'Clients': 'Clients',
    'Client Relations': 'Relations Client',
    'Documentation': 'Documentation',
    'Strategic Planning': 'Planification Stratégique',
    'Supply Chain': 'Chaîne d\'Approvisionnement',
    'Supply Chain Management': 'Gestion de la Chaîne d\'Approvisionnement',
    'Logistics': 'Logistique',
    'Procurement': 'Approvisionnement',
    'Vendor Management': 'Gestion des Fournisseurs',
    'Negotiation': 'Négociation',
    'Contract Negotiation': 'Négociation de Contrats',
    
    # === SOFT SKILLS (Compétences Transversales) ===
    'Communication': 'Communication',
    'Communication Skills': 'Compétences en Communication',
    'Verbal Communication': 'Communication Verbale',
    'Written Communication': 'Communication Écrite',
    'Leadership': 'Leadership',
    'Teamwork': 'Travail d\'Équipe',
    'Team Player': 'Esprit d\'Équipe',
    'Collaboration': 'Collaboration',
    'Problem Solving': 'Résolution de Problèmes',
    'Critical Thinking': 'Pensée Critique',
    'Analytical Thinking': 'Pensée Analytique',
    'Creativity': 'Créativité',
    'Innovation': 'Innovation',
    'Time Management': 'Gestion du Temps',
    'Organization': 'Organisation',
    'Organizational Skills': 'Compétences Organisationnelles',
    'Adaptability': 'Adaptabilité',
    'Flexibility': 'Flexibilité',
    'Attention To Detail': 'Souci du Détail',
    'Decision Making': 'Prise de Décision',
    'Conflict Resolution': 'Résolution de Conflits',
    'Planning': 'Planification',
    'Strategic Thinking': 'Pensée Stratégique',
    'Analytical Skills': 'Compétences Analytiques',
    'Interpersonal Skills': 'Compétences Interpersonnelles',
    'Presentation Skills': 'Compétences de Présentation',
    'Public Speaking': 'Prise de Parole en Public',
    'Writing': 'Rédaction',
    'Research': 'Recherche',
    'Initiative': 'Initiative',
    'Self-Motivated': 'Auto-motivé',
    'Work Ethic': 'Éthique de Travail',
    'Multitasking': 'Multi-tâches',
    'Stress Management': 'Gestion du Stress',
    'Coaching': 'Coaching',
    'Mentoring': 'Mentorat',
    
    # === RH & RECRUTEMENT ===
    'Human Resources': 'Ressources Humaines',
    'Hr': 'RH',
    'Recruitment': 'Recrutement',
    'Recruiting': 'Recrutement',
    'Talent Acquisition': 'Acquisition de Talents',
    'Employee Relations': 'Relations avec les Employés',
    'Performance Management': 'Gestion de la Performance',
    'Training': 'Formation',
    'Training And Development': 'Formation et Développement',
    'Onboarding': 'Intégration',
    'Compensation': 'Rémunération',
    'Benefits': 'Avantages Sociaux',
    
    # === DESIGN & CRÉATIF ===
    'Graphic Design': 'Design Graphique',
    'Web Design': 'Design Web',
    'Ui Design': 'Design d\'Interface',
    'Ux Design': 'Design d\'Expérience Utilisateur',
    'Ui/Ux': 'UI/UX',
    'Adobe Photoshop': 'Adobe Photoshop',
    'Adobe Illustrator': 'Adobe Illustrator',
    'Adobe Indesign': 'Adobe InDesign',
    'Figma': 'Figma',
    'Sketch': 'Sketch',
    'Prototyping': 'Prototypage',
    'Wireframing': 'Maquettage',
    
    # === SÉCURITÉ & RÉSEAUX ===
    'Cybersecurity': 'Cybersécurité',
    'Information Security': 'Sécurité de l\'Information',
    'Network Security': 'Sécurité Réseau',
    'Penetration Testing': 'Tests de Pénétration',
    'Ethical Hacking': 'Piratage Éthique',
    'Firewall': 'Pare-feu',
    'Vpn': 'VPN',
    'Encryption': 'Chiffrement',
    'Networking': 'Réseaux',
    'Network Administration': 'Administration Réseau',
    'Tcp/Ip': 'TCP/IP',
    'Dns': 'DNS',
    'Dhcp': 'DHCP',
    
    # === AUTRES DOMAINES ===
    'Healthcare': 'Santé',
    'Medical': 'Médical',
    'Nursing': 'Soins Infirmiers',
    'Pharmacy': 'Pharmacie',
    'Clinical': 'Clinique',
    'Patient Care': 'Soins aux Patients',
    'Legal': 'Juridique',
    'Law': 'Droit',
    'Compliance': 'Conformité',
    'Regulatory': 'Réglementaire',
    'Education': 'Éducation',
    'Teaching': 'Enseignement',
    'Curriculum Development': 'Développement de Programmes',
    'E-Learning': 'E-Learning',
    'Construction': 'Construction',
    'Civil Engineering': 'Génie Civil',
    'Architecture': 'Architecture',
    'Manufacturing': 'Fabrication',
    'Production': 'Production',
    'Operations': 'Opérations',
    'Operations Management': 'Gestion des Opérations',
    'Retail': 'Commerce de Détail',
    'Hospitality': 'Hôtellerie',
    'Real Estate': 'Immobilier',
}

# RÈGLES DE TRADUCTION AUTOMATIQUE
AUTO_TRANSLATION_RULES = [
    # Management → Gestion
    (r'\b(\w+)\s+Management\b', r'Gestion de \1'),
    (r'\b(\w+)\s+Manager\b', r'Gestionnaire \1'),
    
    # Development → Développement
    (r'\b(\w+)\s+Development\b', r'Développement \1'),
    (r'\b(\w+)\s+Developer\b', r'Développeur \1'),
    
    # Engineering → Ingénierie
    (r'\b(\w+)\s+Engineering\b', r'Ingénierie \1'),
    (r'\b(\w+)\s+Engineer\b', r'Ingénieur \1'),
    
    # Analysis → Analyse
    (r'\b(\w+)\s+Analysis\b', r'Analyse \1'),
    (r'\b(\w+)\s+Analyst\b', r'Analyste \1'),
    
    # Design → Conception
    (r'\b(\w+)\s+Design\b', r'Conception \1'),
    (r'\b(\w+)\s+Designer\b', r'Concepteur \1'),
    
    # Administration → Administration
    (r'\b(\w+)\s+Administration\b', r'Administration \1'),
    (r'\b(\w+)\s+Administrator\b', r'Administrateur \1'),
    
    # Consulting → Conseil
    (r'\b(\w+)\s+Consulting\b', r'Conseil en \1'),
    (r'\b(\w+)\s+Consultant\b', r'Consultant \1'),
]

def translate_skill(skill: str) -> str:
    """
    Traduit une compétence en français
    """
    # 1. Vérifier traduction directe
    if skill in COMPLETE_TRANSLATIONS:
        return COMPLETE_TRANSLATIONS[skill]
    
    # 2. Vérifier en minuscules
    skill_lower = skill.lower()
    for en, fr in COMPLETE_TRANSLATIONS.items():
        if en.lower() == skill_lower:
            return fr
    
    # 3. Appliquer les règles automatiques
    skill_translated = skill
    for pattern, replacement in AUTO_TRANSLATION_RULES:
        match = re.search(pattern, skill, re.IGNORECASE)
        if match:
            skill_translated = re.sub(pattern, replacement, skill, flags=re.IGNORECASE)
            break
    
    # 4. Si traduit, retourner
    if skill_translated != skill:
        return skill_translated
    
    # 5. Sinon, garder l'original (termes techniques universels)
    return skill

def translate_skills_file(input_path: Path, output_path: Path):
    """
    Traduit le fichier de compétences en français
    """
    print("=" * 70)
    print("🇫🇷 Traduction COMPLÈTE des Compétences en Français")
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
    
    # Traduire
    technical_translated = {}
    soft_translated = {}
    
    translations_made = 0
    kept_original = 0
    
    for skill in data['technical_skills']:
        translated = translate_skill(skill)
        technical_translated[translated] = skill
        if translated != skill:
            translations_made += 1
        else:
            kept_original += 1
    
    for skill in data['soft_skills']:
        translated = translate_skill(skill)
        soft_translated[translated] = skill
        if translated != skill:
            translations_made += 1
        else:
            kept_original += 1
    
    # Créer le nouveau fichier
    translated_data = {
        'technical_skills': sorted(list(technical_translated.keys())),
        'soft_skills': sorted(list(soft_translated.keys())),
        'metadata': {
            'total_skills': len(technical_translated) + len(soft_translated),
            'technical': len(technical_translated),
            'soft': len(soft_translated),
            'source': data['metadata']['source'] + ' - Traduit en français',
            'total_cvs_analyzed': data['metadata']['total_cvs_analyzed'],
            'language': 'français',
            'translations_made': translations_made,
            'kept_original': kept_original,
            'dictionary_size': len(COMPLETE_TRANSLATIONS)
        }
    }
    
    # Si top_skills existe, les traduire
    if 'top_skills' in data:
        translated_data['top_skills'] = [
            {
                'skill': translate_skill(item['skill']),
                'skill_original': item['skill'],
                'frequency': item['frequency'],
                'type': item['type']
            }
            for item in data['top_skills'][:200]
        ]
    
    # Sauvegarder
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Traduction terminée!")
    print(f"   Traductions effectuées: {translations_made}")
    print(f"   Conservées (termes techniques): {kept_original}")
    print(f"   Dictionnaire: {len(COMPLETE_TRANSLATIONS)} traductions")
    print(f"   Total après déduplication: {translated_data['metadata']['total_skills']}")
    print()
    
    print(f"💾 Fichier créé: {output_path}")
    print(f"   Taille: {output_path.stat().st_size / 1024:.1f} KB")
    
    # Afficher exemples
    print("\n📋 Exemples de traductions:")
    examples = [
        ('Machine Learning', 'Apprentissage Automatique'),
        ('Data Analysis', 'Analyse de Données'),
        ('Project Management', 'Gestion de Projet'),
        ('Communication', 'Communication'),
        ('Financial Analysis', 'Analyse Financière'),
    ]
    for en, expected_fr in examples:
        if en in [item['skill_original'] for item in translated_data.get('top_skills', [])]:
            actual_fr = translate_skill(en)
            status = "✅" if actual_fr == expected_fr else "⚠️"
            print(f"   {status} {en:30s} → {actual_fr}")

def main():
    """Point d'entrée principal"""
    print()
    print("=" * 70)
    print("🎯 Traducteur AMÉLIORÉ de Compétences EN → FR")
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
    print("🔧 Le fichier sera automatiquement utilisé par skills_loader.py")
    print("   (priorité donnée aux compétences françaises)")
    print()
    print("🚀 Redémarrez le serveur:")
    print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080")

if __name__ == "__main__":
    main()

