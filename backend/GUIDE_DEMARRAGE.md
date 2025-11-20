# 🚀 Guide de Démarrage - Backend SmartHire

## ✅ Ce qui a été créé

Le backend FastAPI complet avec :

### 📁 Structure complète
- ✅ Configuration et settings (`.env`, `config.py`)
- ✅ Connexion PostgreSQL (SQLAlchemy)
- ✅ 3 Models : User, CV, ScrapedOffer
- ✅ Schemas Pydantic pour validation
- ✅ Authentification JWT complète
- ✅ 4 routers API (auth, users, cvs, offers)
- ✅ Web scraping Rekrute.com
- ✅ Upload de fichiers (CV, photos)

### 🛣️ Endpoints disponibles (15 endpoints)

#### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion (obtenir token JWT)
- `GET /api/auth/me` - Profil utilisateur connecté

#### Gestion utilisateur
- `PUT /api/users/profile` - Modifier profil
- `POST /api/users/photo` - Upload photo de profil
- `GET /api/users/{user_id}/photo` - Récupérer photo

#### Gestion CV
- `POST /api/cvs/upload` - Upload un CV (PDF/image)
- `GET /api/cvs/me` - Liste de mes CVs
- `DELETE /api/cvs/{cv_id}` - Supprimer un CV

#### Offres d'emploi
- `GET /api/offers` - Liste des offres (filtres: ville, type_contrat)
- `GET /api/offers/search` - Recherche par mots-clés
- `GET /api/offers/{offer_id}` - Détails d'une offre
- `POST /api/offers/scrape` - Lancer scraping manuel

#### Utilitaires
- `GET /` - Message d'accueil
- `GET /health` - Health check

---

## 🔧 INSTALLATION - Étape par étape

### Prérequis
- Python 3.9+
- PostgreSQL 13+
- pip

### Étape 1 : Base de données PostgreSQL

**Option A : Créer avec psql**
```bash
psql -U postgres
CREATE DATABASE smarthire_db;
\q
```

**Option B : Avec createdb**
```bash
createdb -U postgres smarthire_db
```

**Vérifier la création :**
```bash
psql -U postgres -l | grep smarthire
```

### Étape 2 : Configuration de l'environnement

Le fichier `.env` a été créé automatiquement avec ces valeurs par défaut :

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/smarthire_db
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

UPLOAD_DIR=./uploads
AVATAR_DIR=./uploads/avatars
CV_DIR=./uploads/cvs
MAX_UPLOAD_SIZE=10485760

SCRAPING_ENABLED=true
SCRAPING_MAX_OFFERS=50
```

**⚠️ IMPORTANT : Modifier ces valeurs si nécessaire**

Si votre PostgreSQL a un mot de passe différent, modifiez `DATABASE_URL` :
```
DATABASE_URL=postgresql://VOTRE_USER:VOTRE_PASSWORD@localhost:5432/smarthire_db
```

### Étape 3 : Environnement virtuel Python

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer (Windows PowerShell)
venv\Scripts\Activate.ps1

# Activer (Windows CMD)
venv\Scripts\activate.bat

# Activer (Linux/Mac)
source venv/bin/activate
```

### Étape 4 : Installer les dépendances

```bash
cd backend
pip install -r requirements.txt
```

**Packages installés :**
- fastapi, uvicorn (serveur)
- sqlalchemy, psycopg2-binary (base de données)
- python-jose, passlib (authentification)
- beautifulsoup4, requests (scraping)
- pydantic, pillow, etc.

### Étape 5 : Créer les dossiers uploads

```bash
# Windows PowerShell
New-Item -ItemType Directory -Force -Path uploads\avatars
New-Item -ItemType Directory -Force -Path uploads\cvs

# Linux/Mac
mkdir -p uploads/avatars uploads/cvs
```

### Étape 6 : Lancer le serveur

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Vous devriez voir :**
```
==================================================
🚀 SmartHire API Started
==================================================
📚 Documentation: http://localhost:8000/docs
🔍 Alternative docs: http://localhost:8000/redoc
💾 Database: localhost:5432/smarthire_db
==================================================

INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🧪 TESTER L'API

### Option 1 : Interface Swagger (Recommandé)

1. Ouvrir http://localhost:8000/docs
2. Tester chaque endpoint visuellement

### Option 2 : Avec curl (Terminal)

#### 1. S'inscrire
```bash
curl -X POST http://localhost:8000/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"nom\":\"SERRAJ\",\"prenom\":\"Ranya\",\"email\":\"ranya@test.com\",\"mot_de_passe\":\"password123\"}"
```

**Réponse attendue :**
```json
{
  "id": 1,
  "nom": "SERRAJ",
  "prenom": "Ranya",
  "email": "ranya@test.com",
  "telephone": null,
  "photo_profil": null,
  "ville_preferee": null,
  "created_at": "2025-11-19T...",
  "updated_at": "2025-11-19T..."
}
```

#### 2. Se connecter
```bash
curl -X POST http://localhost:8000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"ranya@test.com\",\"mot_de_passe\":\"password123\"}"
```

**Réponse :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**💾 COPIER LE TOKEN** pour les prochaines requêtes !

#### 3. Récupérer son profil (avec token)
```bash
# Remplacer YOUR_TOKEN par le token reçu
curl -X GET http://localhost:8000/api/auth/me ^
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 4. Modifier son profil
```bash
curl -X PUT http://localhost:8000/api/users/profile ^
  -H "Authorization: Bearer YOUR_TOKEN" ^
  -H "Content-Type: application/json" ^
  -d "{\"telephone\":\"+212 6XX XX XX XX\",\"ville_preferee\":\"Rabat\"}"
```

#### 5. Upload un CV
```bash
curl -X POST http://localhost:8000/api/cvs/upload ^
  -H "Authorization: Bearer YOUR_TOKEN" ^
  -F "file=@chemin/vers/votre/cv.pdf"
```

#### 6. Liste de mes CVs
```bash
curl -X GET http://localhost:8000/api/cvs/me ^
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 7. Lancer le scraping d'offres
```bash
curl -X POST http://localhost:8000/api/offers/scrape
```

#### 8. Récupérer les offres
```bash
# Toutes les offres
curl -X GET http://localhost:8000/api/offers

# Filtrer par ville
curl -X GET "http://localhost:8000/api/offers?ville=Casablanca&limit=10"

# Rechercher
curl -X GET "http://localhost:8000/api/offers/search?q=développeur&ville=Rabat"
```

### Option 3 : Script Python de test

Créer un fichier `test_api.py` :

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Inscription
print("1. Inscription...")
response = requests.post(
    f"{BASE_URL}/api/auth/register",
    json={
        "nom": "Test",
        "prenom": "User",
        "email": "test@example.com",
        "mot_de_passe": "test123"
    }
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# 2. Connexion
print("2. Connexion...")
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "email": "test@example.com",
        "mot_de_passe": "test123"
    }
)
token = response.json()["access_token"]
print(f"Token reçu: {token[:50]}...\n")

# 3. Profil
print("3. Récupération du profil...")
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
print(f"Profil: {response.json()}\n")

# 4. Offres
print("4. Liste des offres...")
response = requests.get(f"{BASE_URL}/api/offers")
print(f"Nombre d'offres: {len(response.json())}")
```

Lancer :
```bash
python test_api.py
```

---

## 🗄️ Base de données - Tables créées

### Table `users`
```sql
id              SERIAL PRIMARY KEY
nom             VARCHAR(100) NOT NULL
prenom          VARCHAR(100) NOT NULL
email           VARCHAR(255) UNIQUE NOT NULL
mot_de_passe    VARCHAR(255) NOT NULL (hashé bcrypt)
telephone       VARCHAR(20)
photo_profil    VARCHAR(255)
ville_preferee  VARCHAR(100)
created_at      TIMESTAMP DEFAULT NOW()
updated_at      TIMESTAMP DEFAULT NOW()
```

### Table `cvs`
```sql
id                      SERIAL PRIMARY KEY
user_id                 INTEGER REFERENCES users(id) ON DELETE CASCADE
nom_fichier             VARCHAR(255) NOT NULL
type_fichier            VARCHAR(10) NOT NULL
chemin_fichier          VARCHAR(255) NOT NULL
contenu_texte           TEXT
nom_complet             VARCHAR(200)
email_cv                VARCHAR(255)
telephone_cv            VARCHAR(20)
competences_extraites   JSONB
date_upload             TIMESTAMP DEFAULT NOW()
created_at              TIMESTAMP DEFAULT NOW()
```

### Table `scraped_offers`
```sql
id                      SERIAL PRIMARY KEY
titre                   VARCHAR(255) NOT NULL
entreprise              VARCHAR(200)
description             TEXT NOT NULL
localisation            VARCHAR(100)
ville                   VARCHAR(100)
type_contrat            VARCHAR(50)
salaire                 VARCHAR(100)
url_source              TEXT UNIQUE NOT NULL
source_site             VARCHAR(50) NOT NULL
date_publication        DATE
competences_requises    JSONB
competences_souhaitees  JSONB
est_active              BOOLEAN DEFAULT TRUE
date_scraping           TIMESTAMP DEFAULT NOW()
created_at              TIMESTAMP DEFAULT NOW()
```

**Vérifier les tables :**
```bash
psql -U postgres -d smarthire_db -c "\dt"
```

---

## 🔐 Authentification JWT - Comment ça marche ?

1. **Inscription** : `POST /api/auth/register`
   - Mot de passe hashé avec bcrypt
   - Utilisateur créé en DB

2. **Connexion** : `POST /api/auth/login`
   - Vérification email + mot de passe
   - Génération d'un JWT token (expire après 24h)
   - Token contient : `{"sub": "email@example.com", "exp": timestamp}`

3. **Utilisation** : Ajouter header à chaque requête protégée
   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

4. **Vérification** : Backend décode le token, extrait l'email, récupère l'utilisateur

---

## 🕷️ Web Scraping

### Scraper Rekrute.com

Le scraper `RekruteScraper` :
- URL : https://www.rekrute.com/offres.html
- Limite : 50 offres (configurable dans `.env`)
- Extrait : titre, entreprise, ville, description, URL
- Évite les doublons (par URL unique)

**Lancer manuellement :**
```bash
curl -X POST http://localhost:8000/api/offers/scrape
```

**Réponse :**
```json
{
  "status": "success",
  "offers_found": 45,
  "offers_saved": 45
}
```

**Note :** Le sélecteur CSS peut nécessiter des ajustements selon la structure réelle du site.

---

## 📦 Upload de fichiers

### Photos de profil
- **Formats** : JPG, JPEG, PNG
- **Taille max** : 5MB
- **Stockage** : `uploads/avatars/{user_id}_{timestamp}.ext`
- **Endpoint** : `POST /api/users/photo`

### CVs
- **Formats** : PDF, JPG, JPEG, PNG
- **Taille max** : 10MB (configurable)
- **Stockage** : `uploads/cvs/{user_id}_{timestamp}.ext`
- **Endpoint** : `POST /api/cvs/upload`

---

## 🚨 Troubleshooting

### Erreur : "ModuleNotFoundError: No module named 'app'"

**Solution :**
```bash
# S'assurer d'être dans le dossier backend/
cd backend
# Réinstaller
pip install -r requirements.txt
```

### Erreur : "FATAL: password authentication failed"

**Solution :** Modifier `.env` avec vos identifiants PostgreSQL corrects

### Erreur : "could not connect to server"

**Solution :** Vérifier que PostgreSQL est démarré
```bash
# Windows
pg_ctl status

# Linux
sudo systemctl status postgresql
```

### Erreur : "Permission denied: './uploads'"

**Solution :**
```bash
mkdir -p uploads/avatars uploads/cvs
chmod 755 uploads
```

### Port 8000 déjà utilisé

**Solution :** Utiliser un autre port
```bash
uvicorn app.main:app --reload --port 8001
```

---

## 🔄 Connecter le Frontend

### 1. Dans le frontend, créer un fichier `lib/api.ts` :

```typescript
const API_URL = "http://localhost:8000";

export async function login(email: string, password: string) {
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, mot_de_passe: password }),
  });
  return response.json();
}

export async function getProfile(token: string) {
  const response = await fetch(`${API_URL}/api/auth/me`, {
    headers: { "Authorization": `Bearer ${token}` },
  });
  return response.json();
}

export async function uploadCV(file: File, token: string) {
  const formData = new FormData();
  formData.append("file", file);
  
  const response = await fetch(`${API_URL}/api/cvs/upload`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
    body: formData,
  });
  return response.json();
}
```

### 2. Modifier `contexts/AuthContext.tsx` :

Changer `USE_MOCK_AUTH` à `false` et remplacer les fetch par des appels au backend :

```typescript
const USE_MOCK_AUTH = false; // Utiliser le vrai backend

const login = async (email: string, password: string) => {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, mot_de_passe: password })
  });
  
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  
  // Récupérer le profil
  const profileResponse = await fetch('http://localhost:8000/api/auth/me', {
    headers: { 'Authorization': `Bearer ${data.access_token}` }
  });
  const userData = await profileResponse.json();
  
  setUser(userData);
};
```

---

## 📊 Données de test

### Créer un utilisateur de test

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nom":"SERRAJ","prenom":"Ranya","email":"ranya@test.com","mot_de_passe":"test123"}'
```

### Insérer des offres de test (SQL)

```sql
INSERT INTO scraped_offers (titre, entreprise, description, ville, type_contrat, url_source, source_site, est_active)
VALUES 
  ('Développeur Full Stack', 'TechVision', 'Recherche dev Full Stack avec React et Node.js', 'Casablanca', 'CDI', 'https://example.com/1', 'rekrute', true),
  ('Data Scientist', 'DataCorp', 'Expert en ML et Python', 'Rabat', 'CDI', 'https://example.com/2', 'rekrute', true),
  ('DevOps Engineer', 'CloudTech', 'AWS, Docker, Kubernetes', 'Tanger', 'CDI', 'https://example.com/3', 'rekrute', true);
```

---

## 🎯 Prochaines étapes (Phase 2)

1. **Extraction de texte des CVs**
   - PDF : PyPDF2 ou pdfplumber
   - Images : Tesseract OCR

2. **Analyse NLP avec spaCy**
   - Extraction des compétences
   - Détection des soft skills
   - NER personnalisé

3. **Matching CV/Offre**
   - TF-IDF ou Sentence-BERT
   - Calcul de score de similarité
   - Machine Learning pour recommandations

4. **Génération de lettres**
   - Intégration OpenAI GPT ou Hugging Face
   - Templates personnalisables

5. **Scraping avancé**
   - Selenium pour sites dynamiques
   - Celery pour tâches async
   - Cron jobs quotidiens

---

## 📚 Ressources

- **FastAPI Docs** : https://fastapi.tiangolo.com/
- **SQLAlchemy** : https://docs.sqlalchemy.org/
- **JWT** : https://jwt.io/
- **PostgreSQL** : https://www.postgresql.org/docs/

---

## ✅ Checklist finale

- [ ] PostgreSQL installé et smarthire_db créé
- [ ] `.env` configuré avec bonnes credentials
- [ ] Dépendances Python installées
- [ ] Dossiers uploads/ créés
- [ ] Serveur démarre sans erreur
- [ ] Documentation Swagger accessible
- [ ] Test d'inscription fonctionne
- [ ] Test de login retourne un token
- [ ] Upload de CV fonctionne
- [ ] Scraping retourne des offres

**Si tous les checks ✅ → Backend prêt pour connexion avec le frontend !**


