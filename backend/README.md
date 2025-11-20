# SmartHire Backend API

Backend FastAPI pour la plateforme SmartHire - Analyse de CV et matching d'offres d'emploi.

## 🚀 Installation

### 1. Créer la base de données PostgreSQL

```bash
# Créer la base de données
createdb smarthire_db

# Ou avec psql
psql -U postgres
CREATE DATABASE smarthire_db;
\q
```

### 2. Configurer l'environnement

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et configurer vos paramètres
nano .env
```

**Important**: Changez au minimum :
- `DATABASE_URL` avec vos identifiants PostgreSQL
- `SECRET_KEY` avec une clé aléatoire longue

### 3. Installer les dépendances

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows:
venv\Scripts\activate
# Sur Linux/Mac:
source venv/bin/activate

# Installer les packages
pip install -r requirements.txt
```

### 4. Créer les dossiers uploads

```bash
mkdir -p uploads/avatars uploads/cvs
```

### 5. Lancer le serveur

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Le serveur démarre sur `http://localhost:8000`

## 📚 Documentation

Une fois le serveur lancé :
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification.

### Workflow d'authentification :

1. **S'inscrire** : `POST /api/auth/register`
2. **Se connecter** : `POST /api/auth/login` → Reçoit un token
3. **Utiliser le token** : Ajouter header `Authorization: Bearer {token}`

## 📁 Structure du projet

```
backend/
├── app/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py            # Configuration
│   ├── database.py          # Connexion PostgreSQL
│   │
│   ├── models/              # Models SQLAlchemy
│   │   ├── user.py
│   │   ├── cv.py
│   │   └── offer.py
│   │
│   ├── schemas/             # Schemas Pydantic
│   │   ├── user.py
│   │   ├── cv.py
│   │   └── offer.py
│   │
│   ├── api/                 # Routes API
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── cvs.py
│   │   └── offers.py
│   │
│   ├── core/                # Utilitaires
│   │   ├── security.py
│   │   └── deps.py
│   │
│   └── scrapers/            # Web scraping
│       ├── base_scraper.py
│       └── rekrute_scraper.py
│
├── uploads/                 # Fichiers uploadés
│   ├── avatars/
│   └── cvs/
│
├── .env                     # Variables d'environnement
├── requirements.txt
└── README.md
```

## 🛣️ Endpoints disponibles

### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `GET /api/auth/me` - Profil utilisateur

### Utilisateurs
- `PUT /api/users/profile` - Mettre à jour le profil
- `POST /api/users/photo` - Upload photo de profil
- `GET /api/users/{user_id}/photo` - Récupérer photo

### CVs
- `POST /api/cvs/upload` - Upload un CV
- `GET /api/cvs/me` - Liste de mes CVs
- `DELETE /api/cvs/{cv_id}` - Supprimer un CV

### Offres d'emploi
- `GET /api/offers` - Liste des offres
- `GET /api/offers/search` - Rechercher des offres
- `GET /api/offers/{offer_id}` - Détails d'une offre
- `POST /api/offers/scrape` - Lancer le scraping (admin)

## 🗄️ Base de données

### Tables créées

1. **users** - Utilisateurs
2. **cvs** - CVs uploadés
3. **scraped_offers** - Offres scrapées

### Migrations

Les tables sont créées automatiquement au démarrage.

Pour des migrations plus complexes, utiliser Alembic :

```bash
# Initialiser Alembic
alembic init alembic

# Créer une migration
alembic revision --autogenerate -m "Description"

# Appliquer les migrations
alembic upgrade head
```

## 🕷️ Web Scraping

Le scraping des offres d'emploi est inclus.

### Lancer le scraping manuellement

```bash
curl -X POST http://localhost:8000/api/offers/scrape
```

Ou via l'interface Swagger : http://localhost:8000/docs

### Activer/désactiver le scraping

Dans `.env` :
```
SCRAPING_ENABLED=true
SCRAPING_MAX_OFFERS=50
```

## 🧪 Tester l'API

### Avec curl

```bash
# S'inscrire
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nom":"Doe","prenom":"John","email":"john@example.com","mot_de_passe":"password123"}'

# Se connecter
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","mot_de_passe":"password123"}'

# Utiliser le token
TOKEN="votre_token_ici"
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Avec Python

```python
import requests

# S'inscrire
response = requests.post(
    "http://localhost:8000/api/auth/register",
    json={
        "nom": "Doe",
        "prenom": "John",
        "email": "john@example.com",
        "mot_de_passe": "password123"
    }
)
print(response.json())

# Se connecter
response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={
        "email": "john@example.com",
        "mot_de_passe": "password123"
    }
)
token = response.json()["access_token"]

# Utiliser le token
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:8000/api/auth/me",
    headers=headers
)
print(response.json())
```

## 🔧 Configuration avancée

### Variables d'environnement

Voir `.env.example` pour toutes les options disponibles.

### Sécurité

- Les mots de passe sont hashés avec bcrypt
- Les tokens JWT expirent après 24h (configurable)
- Les fichiers uploadés sont validés (type, taille)

## 🚨 Troubleshooting

### Erreur de connexion à PostgreSQL

```
FATAL: password authentication failed
```

→ Vérifiez `DATABASE_URL` dans `.env`

### Erreur de permissions sur uploads/

```
Permission denied: './uploads'
```

→ Créez le dossier manuellement :
```bash
mkdir -p uploads/avatars uploads/cvs
chmod 755 uploads
```

### Module not found

```
ModuleNotFoundError: No module named 'xxx'
```

→ Réinstallez les dépendances :
```bash
pip install -r requirements.txt
```

## 📝 Notes de développement

- Le serveur se recharge automatiquement avec `--reload`
- Les logs sont affichés dans la console
- Les erreurs SQL sont affichées en mode debug

## 🎯 Prochaines étapes

Phase 2 incluera :
- Extraction de texte des CVs (OCR, PDF parsing)
- Analyse de CV avec NLP (spaCy)
- Matching CV/Offre avec ML
- Génération de lettres de motivation (GPT)
- Système de recommandation

## 📧 Support

Pour toute question, consultez la documentation Swagger ou contactez l'équipe de développement.
