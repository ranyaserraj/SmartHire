# 🎯 SmartHire - Plateforme Intelligente de Gestion de CV et Recherche d'Emploi

SmartHire est une application web moderne qui utilise l'intelligence artificielle pour aider les candidats à optimiser leurs CV, rechercher des emplois et gérer leurs candidatures.

## 🌟 Fonctionnalités Principales

### 📄 Gestion de CV
- **Upload et analyse de CV** avec extraction automatique des informations
- **Score de compatibilité** avec les offres d'emploi
- **Suggestions d'amélioration** personnalisées basées sur l'IA
- **Analyse avancée** des compétences techniques et soft skills
- **Historique des analyses** avec comparaison dans le temps

### 🔍 Recherche d'Emploi Intelligente
- **Recommandations personnalisées** basées sur votre profil
- **Recherche avancée** avec filtres multiples
- **Scraping automatique** des offres depuis les principales plateformes marocaines
- **Alertes emploi** configurables par critères

### 📊 Tableau de Bord Analytique
- **Statistiques détaillées** sur vos candidatures
- **Évolution du score** de votre CV dans le temps
- **Analyse comparative** de vos compétences vs. le marché
- **Heatmap des compétences** par ville
- **Tendances du marché** de l'emploi

### 📝 Lettres de Motivation
- **Génération automatique** adaptée à chaque offre
- **3 versions** : Formelle, Dynamique, Créative
- **Email d'accompagnement** pré-rempli
- **Préparation aux entretiens** avec questions probables

### 🎯 Suivi des Candidatures
- **Tableau Kanban** pour suivre l'avancement
- **Timeline détaillée** de chaque candidature
- **Prise de notes** et rappels
- **Statistiques** de performance

## 🛠️ Technologies Utilisées

### Frontend
- **Next.js 14** - Framework React avec App Router
- **TypeScript** - Typage statique
- **Tailwind CSS** - Styling moderne et responsive
- **Shadcn/UI** - Composants UI réutilisables
- **Recharts** - Visualisation de données
- **Lucide React** - Icônes modernes

### Backend
- **FastAPI** - Framework Python moderne et rapide
- **PostgreSQL** - Base de données relationnelle
- **SQLAlchemy** - ORM Python
- **Pydantic** - Validation de données
- **JWT** - Authentification sécurisée
- **Bcrypt** - Hachage de mots de passe

### Outils & Services
- **BeautifulSoup4** - Scraping web
- **Python Multipart** - Gestion des uploads
- **CORS** - Cross-Origin Resource Sharing

## 📋 Prérequis

- Node.js 18+ et npm/pnpm
- Python 3.10+
- PostgreSQL 14+

## 🚀 Installation et Démarrage

### 1. Cloner le repository

```bash
git clone https://github.com/ranyaserraj/SmartHire.git
cd SmartHire
```

### 2. Configuration de la Base de Données

Créez une base de données PostgreSQL :

```sql
CREATE DATABASE smarthire;
```

### 3. Configuration du Backend

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env (ou utiliser create_env.bat)
# DATABASE_URL=postgresql://postgres:votre_mot_de_passe@localhost/smarthire
# SECRET_KEY=votre_secret_key_tres_longue_et_securisee
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30

# Exécuter les migrations SQL
psql -U postgres -d smarthire -f alembic_migration.sql

# Démarrer le serveur (ou utiliser START_SERVER.bat)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Le backend sera accessible sur `http://localhost:8080`
Documentation API : `http://localhost:8080/docs`

### 4. Configuration du Frontend

```bash
# Retourner à la racine du projet
cd ..

# Installer les dépendances
npm install
# ou
pnpm install

# Démarrer le serveur de développement
npm run dev
# ou
pnpm dev
```

Le frontend sera accessible sur `http://localhost:3000`

## 📁 Structure du Projet

```
SmartHire/
├── app/                      # Pages Next.js (App Router)
│   ├── dashboard/           # Pages du tableau de bord
│   ├── auth/               # Authentification
│   ├── results/            # Résultats d'analyse
│   ├── analytics/          # Tableaux analytiques
│   └── ...
├── components/              # Composants React réutilisables
│   ├── dashboard/          # Composants du dashboard
│   ├── layouts/            # Layouts globaux
│   ├── ui/                 # Composants UI de base
│   └── ...
├── contexts/               # Contextes React (Auth, etc.)
├── hooks/                  # Hooks personnalisés
├── lib/                    # Utilitaires
├── public/                 # Assets statiques
├── backend/                # Backend FastAPI
│   ├── app/
│   │   ├── api/           # Endpoints API
│   │   ├── models/        # Modèles SQLAlchemy
│   │   ├── schemas/       # Schémas Pydantic
│   │   ├── core/          # Configuration & sécurité
│   │   └── scrapers/      # Scrapers de sites d'emploi
│   ├── uploads/           # Fichiers uploadés
│   └── ...
└── ...
```

## 🔐 Authentification

L'application utilise JWT pour l'authentification. Lors de l'inscription, les utilisateurs fournissent :
- Nom et prénom
- Email
- Mot de passe sécurisé
- Téléphone
- Ville préférée
- Photo de profil (optionnel)

## 📊 Fonctionnalités à Venir

- [ ] Intégration avec LinkedIn
- [ ] Chat IA pour conseils carrière
- [ ] Suivi des statistiques de candidatures en temps réel
- [ ] Export PDF des analyses
- [ ] Notifications push
- [ ] Mode hors ligne

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📝 Licence

Ce projet est sous licence MIT.

## 👥 Auteurs

- **Ranya Serraj** - [GitHub](https://github.com/ranyaserraj)

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

---

**SmartHire** - Votre partenaire intelligent pour une recherche d'emploi réussie ! 🚀

