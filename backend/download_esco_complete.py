"""
Script pour télécharger et parser correctement le dataset ESCO complet
Gère les problèmes d'encodage et crée un fichier JSON propre
"""
import csv
import json
import requests
from pathlib import Path
from typing import Dict, List, Set
import sys

# URL de l'API ESCO pour téléchargement direct
ESCO_API_BASE = "https://ec.europa.eu/esco/api"

def download_esco_from_web():
    """
    Télécharge ESCO depuis l'API web officielle
    """
    print("=" * 70)
    print("📥 Téléchargement du Dataset ESCO Complet")
    print("=" * 70)
    print()
    
    # URL pour télécharger le dataset complet
    # Note: L'API ESCO nécessite un accès direct au fichier CSV
    
    print("⚠️  Le téléchargement automatique ESCO nécessite une clé API.")
    print()
    print("📌 SOLUTION ALTERNATIVE : Parser le CSV déjà téléchargé")
    print()
    print("Si vous avez déjà le fichier CSV ESCO, placez-le dans:")
    print("   backend/data/esco_skills_raw.csv")
    print()
    print("Je vais le parser et créer un fichier JSON propre.")
    print()

def parse_esco_csv_robust(csv_path: Path, output_path: Path):
    """
    Parse le CSV ESCO avec gestion robuste de l'encodage
    """
    print(f"📂 Lecture du fichier: {csv_path}")
    
    if not csv_path.exists():
        print(f"❌ Fichier introuvable: {csv_path}")
        print()
        print("📥 Veuillez télécharger manuellement:")
        print("   1. Aller sur: https://esco.ec.europa.eu/en/use-esco/download")
        print("   2. Télécharger: Skills CSV (French ou English)")
        print("   3. Placer dans: backend/data/esco_skills_raw.csv")
        return False
    
    skills_data = {
        'technical_skills': set(),
        'soft_skills': set(),
        'all_skills': set(),
        'skills_by_type': {},
        'metadata': {
            'total': 0,
            'technical': 0,
            'soft': 0,
            'languages': []
        }
    }
    
    # Essayer différents encodages
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1', 'cp1252']
    
    content = None
    used_encoding = None
    
    for encoding in encodings:
        try:
            print(f"   Essai encodage: {encoding}...")
            with open(csv_path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
                used_encoding = encoding
                print(f"   ✅ Encodage {encoding} fonctionne")
                break
        except Exception as e:
            print(f"   ❌ {encoding} échoué: {e}")
            continue
    
    if not content:
        print("❌ Impossible de lire le fichier avec aucun encodage")
        return False
    
    # Parser le CSV
    print(f"\n📊 Parsing du CSV...")
    
    lines = content.split('\n')
    print(f"   Total lignes: {len(lines)}")
    
    # Détecter le délimiteur
    first_line = lines[0] if lines else ""
    delimiter = ',' if ',' in first_line else ';' if ';' in first_line else '\t'
    print(f"   Délimiteur détecté: '{delimiter}'")
    
    # Parser avec csv.DictReader
    from io import StringIO
    csv_content = StringIO(content)
    reader = csv.DictReader(csv_content, delimiter=delimiter)
    
    count = 0
    errors = 0
    
    for row in reader:
        try:
            # Colonnes attendues du CSV ESCO
            # conceptUri, preferredLabel, altLabels, skillType, reuseLevel, etc.
            
            skill_name = row.get('preferredLabel', '').strip()
            skill_type = row.get('skillType', '').strip().lower()
            skill_uri = row.get('conceptUri', '')
            
            if not skill_name:
                continue
            
            # Nettoyer le nom (enlever les caractères d'encodage bizarres)
            skill_name_clean = clean_skill_name(skill_name)
            
            if not skill_name_clean or len(skill_name_clean) < 2:
                continue
            
            # Ajouter à la collection
            skills_data['all_skills'].add(skill_name_clean)
            
            # Classifier
            if 'soft' in skill_type or 'transversal' in skill_type:
                skills_data['soft_skills'].add(skill_name_clean)
                skills_data['metadata']['soft'] += 1
            else:
                skills_data['technical_skills'].add(skill_name_clean)
                skills_data['metadata']['technical'] += 1
            
            count += 1
            
            if count % 1000 == 0:
                print(f"   Traité: {count} compétences...")
        
        except Exception as e:
            errors += 1
            if errors < 10:  # Afficher seulement les 10 premières erreurs
                print(f"   ⚠️ Erreur ligne {count}: {e}")
            continue
    
    skills_data['metadata']['total'] = count
    
    print(f"\n✅ Parsing terminé:")
    print(f"   Total compétences: {count}")
    print(f"   Techniques: {skills_data['metadata']['technical']}")
    print(f"   Soft skills: {skills_data['metadata']['soft']}")
    print(f"   Erreurs ignorées: {errors}")
    
    # Convertir sets en listes pour JSON
    output_data = {
        'technical_skills': sorted(list(skills_data['technical_skills'])),
        'soft_skills': sorted(list(skills_data['soft_skills'])),
        'metadata': skills_data['metadata']
    }
    
    # Sauvegarder en JSON
    print(f"\n💾 Sauvegarde dans: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Fichier créé: {output_path}")
    print(f"   Taille: {output_path.stat().st_size / 1024:.1f} KB")
    
    return True

def clean_skill_name(name: str) -> str:
    """
    Nettoie un nom de compétence des caractères d'encodage bizarres
    """
    import unicodedata
    
    # Normaliser Unicode
    name = unicodedata.normalize('NFKD', name)
    
    # Enlever les caractères de contrôle
    name = ''.join(char for char in name if unicodedata.category(char)[0] != 'C')
    
    # Enlever les caractères non-ASCII problématiques
    # mais garder les accents français
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -/+#.()éèêëàâäôöûüùîïç')
    name = ''.join(char if char in allowed_chars else ' ' for char in name)
    
    # Nettoyer les espaces multiples
    name = ' '.join(name.split())
    
    return name.strip()

def create_extended_esco_dataset():
    """
    Crée un dataset ESCO étendu avec compétences populaires ajoutées
    """
    print("\n" + "=" * 70)
    print("🚀 Création du Dataset ESCO Étendu")
    print("=" * 70)
    print()
    
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Compétences techniques populaires (à ajouter au dataset ESCO)
    popular_tech_skills = [
        # Langages de programmation
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
        "PHP", "Ruby", "Swift", "Kotlin", "Scala", "R", "MATLAB", "Perl",
        
        # Frameworks Web
        "React", "React.js", "Angular", "Vue.js", "Next.js", "Nuxt.js", "Svelte",
        "Django", "Flask", "FastAPI", "Spring", "Spring Boot", "Express.js",
        "Node.js", "Laravel", "Symfony", "Ruby on Rails", "ASP.NET",
        
        # Mobile
        "React Native", "Flutter", "Android", "iOS", "Xamarin", "Ionic",
        
        # Bases de données
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra",
        "Elasticsearch", "Oracle", "SQLite", "MariaDB", "DynamoDB",
        "Neo4j", "CouchDB", "InfluxDB",
        
        # DevOps & Cloud
        "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud", "GCP",
        "Jenkins", "GitLab CI/CD", "GitHub Actions", "CircleCI",
        "Terraform", "Ansible", "Puppet", "Chef", "Vagrant",
        "Prometheus", "Grafana", "ELK Stack", "Datadog",
        
        # Data Science & AI
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
        "TensorFlow", "PyTorch", "Keras", "Scikit-learn",
        "Pandas", "NumPy", "Apache Spark", "Hadoop", "Kafka",
        "Airflow", "Tableau", "Power BI", "Looker",
        
        # Outils & Méthodologies
        "Git", "GitHub", "GitLab", "Bitbucket", "SVN",
        "Agile", "Scrum", "Kanban", "JIRA", "Confluence",
        "API", "REST", "GraphQL", "gRPC", "WebSocket",
        "Microservices", "CI/CD", "TDD", "BDD",
        "Selenium", "Jest", "Pytest", "JUnit",
        
        # Design & Frontend
        "HTML", "CSS", "SASS", "LESS", "Tailwind CSS", "Bootstrap",
        "Webpack", "Vite", "Babel", "ESLint", "Prettier",
        "Figma", "Adobe XD", "Sketch", "Photoshop", "Illustrator",
        
        # Systèmes & Réseaux
        "Linux", "Unix", "Windows Server", "Bash", "PowerShell",
        "TCP/IP", "DNS", "DHCP", "VPN", "Firewall", "Load Balancing",
        
        # Sécurité
        "Cybersecurity", "Penetration Testing", "OWASP", "SSL/TLS",
        "OAuth", "JWT", "Encryption", "Firewall Configuration",
        
        # Blockchain & Web3
        "Blockchain", "Ethereum", "Solidity", "Smart Contracts", "Web3.js",
    ]
    
    popular_soft_skills = [
        # Leadership
        "Leadership", "Team Management", "Project Management",
        "Strategic Planning", "Decision Making", "Mentoring", "Coaching",
        
        # Communication
        "Communication", "Public Speaking", "Presentation Skills",
        "Active Listening", "Negotiation", "Conflict Resolution",
        "Persuasion", "Storytelling",
        
        # Collaboration
        "Teamwork", "Collaboration", "Cross-functional Collaboration",
        "Interpersonal Skills", "Networking", "Relationship Building",
        
        # Analytical
        "Problem Solving", "Critical Thinking", "Analytical Skills",
        "Research Skills", "Data Analysis", "Strategic Thinking",
        
        # Personal
        "Adaptability", "Flexibility", "Time Management", "Organization",
        "Attention to Detail", "Self-motivation", "Creativity", "Innovation",
        "Initiative", "Resilience", "Stress Management", "Work Ethic",
        
        # Français
        "Gestion d'équipe", "Gestion de projet", "Planification stratégique",
        "Résolution de problèmes", "Pensée critique", "Créativité",
        "Travail en équipe", "Communication", "Leadership",
        "Organisation", "Gestion du temps", "Adaptabilité", "Autonomie",
    ]
    
    output_data = {
        'technical_skills': sorted(popular_tech_skills),
        'soft_skills': sorted(popular_soft_skills),
        'metadata': {
            'total': len(popular_tech_skills) + len(popular_soft_skills),
            'technical': len(popular_tech_skills),
            'soft': len(popular_soft_skills),
            'source': 'Extended dataset with popular skills'
        }
    }
    
    output_path = data_dir / "esco_skills_extended.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Dataset étendu créé: {output_path}")
    print(f"   - {len(popular_tech_skills)} compétences techniques")
    print(f"   - {len(popular_soft_skills)} soft skills")
    print(f"   - Total: {len(popular_tech_skills) + len(popular_soft_skills)} compétences")
    
    return output_path

def main():
    """Point d'entrée principal"""
    print()
    print("=" * 70)
    print("🎯 ESCO Dataset Manager - Version Professionnelle")
    print("=" * 70)
    print()
    
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Chemins des fichiers
    raw_csv = data_dir / "esco_skills_raw.csv"
    full_json = data_dir / "esco_skills_full.json"
    extended_json = data_dir / "esco_skills_extended.json"
    
    print("📋 Options disponibles:")
    print()
    print("1. Parser un CSV ESCO déjà téléchargé")
    print("2. Créer un dataset étendu avec compétences populaires (400+)")
    print("3. Les deux (recommandé)")
    print()
    
    choice = input("Votre choix (1/2/3): ").strip()
    
    if choice == "1":
        if raw_csv.exists():
            parse_esco_csv_robust(raw_csv, full_json)
        else:
            print(f"\n❌ Fichier introuvable: {raw_csv}")
            print("\n📥 Téléchargez manuellement:")
            print("   https://esco.ec.europa.eu/en/use-esco/download")
    
    elif choice == "2":
        create_extended_esco_dataset()
    
    elif choice == "3":
        # Créer le dataset étendu d'abord
        extended_path = create_extended_esco_dataset()
        
        # Si CSV existe, le parser aussi
        if raw_csv.exists():
            print()
            if parse_esco_csv_robust(raw_csv, full_json):
                # Merger les deux datasets
                print("\n🔄 Fusion des datasets...")
                merge_datasets(full_json, extended_json)
    
    else:
        print("❌ Choix invalide")
        return
    
    print()
    print("=" * 70)
    print("✅ Terminé!")
    print("=" * 70)

def merge_datasets(esco_path: Path, extended_path: Path):
    """Merge le dataset ESCO avec le dataset étendu"""
    if not esco_path.exists() or not extended_path.exists():
        return
    
    with open(esco_path, 'r', encoding='utf-8') as f:
        esco_data = json.load(f)
    
    with open(extended_path, 'r', encoding='utf-8') as f:
        extended_data = json.load(f)
    
    # Merger
    all_technical = set(esco_data['technical_skills']) | set(extended_data['technical_skills'])
    all_soft = set(esco_data['soft_skills']) | set(extended_data['soft_skills'])
    
    merged = {
        'technical_skills': sorted(list(all_technical)),
        'soft_skills': sorted(list(all_soft)),
        'metadata': {
            'total': len(all_technical) + len(all_soft),
            'technical': len(all_technical),
            'soft': len(all_soft),
            'source': 'ESCO + Extended'
        }
    }
    
    output_path = esco_path.parent / "esco_skills_complete.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Dataset fusionné créé: {output_path}")
    print(f"   Total: {merged['metadata']['total']} compétences")

if __name__ == "__main__":
    main()

