"""
Script pour télécharger et préparer les données ESCO
ESCO = Référentiel européen officiel des compétences (13 000+ skills)
"""
import requests
import json
import csv
from pathlib import Path

ESCO_API_BASE = "https://ec.europa.eu/esco/api"

def download_esco_skills():
    """
    Télécharge les compétences ESCO depuis l'API officielle
    """
    print("Telechargement des competences ESCO...")
    print("   (Referentiel officiel de l'Union Europeenne)")
    print()
    
    # URL de l'API ESCO pour les compétences
    # Note: L'API ESCO est gratuite mais peut nécessiter une clé API
    # Alternative: Télécharger le CSV depuis le site officiel
    
    print("IMPORTANT:")
    print("   Pour utiliser ESCO, vous devez telecharger manuellement:")
    print()
    print("   1. Aller sur: https://esco.ec.europa.eu/en/use-esco/download")
    print("   2. Telecharger 'Skills' en CSV (francais + anglais)")
    print("   3. Placer le fichier dans: backend/data/esco_skills.csv")
    print()
    print("   Le fichier contient:")
    print("   - 13 000+ competences")
    print("   - Traductions FR/EN")
    print("   - Classification hard/soft skills")
    print("   - Competences liees aux metiers")
    print()
    
    # Créer le dossier data
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    print(f"OK Dossier cree: {data_dir}")
    print()
    print("Prochaines etapes:")
    print("   1. Telechargez le CSV ESCO")
    print("   2. Placez-le dans backend/data/")
    print("   3. Executez: python process_esco.py")
    print()

def create_sample_esco_data():
    """
    Créer un échantillon de données ESCO pour tests
    (En attendant le téléchargement du vrai dataset)
    """
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Échantillon de compétences techniques populaires
    sample_skills = {
        "technical_skills": [
            # Langages
            "Python", "JavaScript", "Java", "C++", "C#", "PHP", "Ruby", "Go",
            "TypeScript", "Kotlin", "Swift", "Rust", "R", "Scala", "Perl",
            
            # Frameworks Web
            "React", "Angular", "Vue.js", "Django", "Flask", "FastAPI",
            "Spring", "Express.js", "Node.js", "Laravel", "Symfony", "Rails",
            "Next.js", "Nuxt.js", "Svelte",
            
            # Bases de données
            "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle",
            "SQLite", "MariaDB", "Cassandra", "Elasticsearch", "DynamoDB",
            
            # DevOps & Cloud
            "Docker", "Kubernetes", "Jenkins", "GitLab CI/CD", "GitHub Actions",
            "AWS", "Azure", "Google Cloud", "Terraform", "Ansible", "Vagrant",
            
            # Data & AI
            "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Keras",
            "Apache Spark", "Hadoop", "Airflow", "Kafka", "Tableau", "Power BI",
            "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
            
            # Mobile
            "Android", "iOS", "React Native", "Flutter", "Xamarin",
            
            # Outils
            "Git", "Linux", "Unix", "Agile", "Scrum", "Jira", "Confluence",
            "API", "REST", "GraphQL", "Microservices", "CI/CD",
            "Test-Driven Development", "Selenium", "Jest", "Pytest",
            
            # Design
            "UI/UX Design", "Figma", "Adobe XD", "Sketch", "Photoshop",
            "Illustrator", "InDesign",
        ],
        
        "soft_skills": [
            # Leadership
            "Leadership", "Team Management", "Project Management", "Mentoring",
            "Coaching", "Decision Making", "Strategic Thinking",
            
            # Communication
            "Communication", "Public Speaking", "Presentation Skills",
            "Active Listening", "Negotiation", "Conflict Resolution",
            
            # Collaboration
            "Teamwork", "Collaboration", "Cross-functional Teamwork",
            "Interpersonal Skills", "Networking",
            
            # Analytical
            "Problem Solving", "Critical Thinking", "Analytical Skills",
            "Research Skills", "Data Analysis",
            
            # Personal
            "Adaptability", "Flexibility", "Time Management", "Organization",
            "Attention to Detail", "Self-motivation", "Creativity",
            "Innovation", "Initiative", "Resilience",
            
            # Français
            "Gestion d'équipe", "Gestion de projet", "Communication",
            "Travail en équipe", "Résolution de problèmes", "Créativité",
            "Autonomie", "Adaptabilité", "Organisation", "Leadership",
        ]
    }
    
    # Sauvegarder en JSON
    output_file = data_dir / "esco_skills_sample.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_skills, f, indent=2, ensure_ascii=False)
    
    print(f"OK Fichier d'echantillon cree: {output_file}")
    print(f"   - {len(sample_skills['technical_skills'])} competences techniques")
    print(f"   - {len(sample_skills['soft_skills'])} soft skills")
    print()
    print("Cet echantillon peut etre utilise temporairement")
    print("   Pour le dataset complet ESCO (13 000+ skills):")
    print("   -> Telechargez depuis https://esco.ec.europa.eu/en/use-esco/download")
    
    return output_file


if __name__ == "__main__":
    print("=" * 60)
    print("ESCO - Referentiel Europeen des Competences")
    print("=" * 60)
    print()
    
    download_esco_skills()
    create_sample_esco_data()
    
    print()
    print("=" * 60)
    print("OK Configuration terminee")
    print("=" * 60)

