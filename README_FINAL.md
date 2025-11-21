# 🎯 SmartHire - Plateforme de Recrutement Intelligente

## ✅ Projet Finalisé et Production-Ready

SmartHire est une plateforme de recrutement moderne avec extraction intelligente de CV et matching automatique avec des offres d'emploi.

---

## 🚀 Démarrage Rapide

### **Backend (API)**

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

**Accès :** http://localhost:8080/docs

### **Frontend (Next.js)**

```bash
npm run dev
```

**Accès :** http://localhost:3000

---

## 📊 Fonctionnalités Principales

### **1. Extraction de CV Intelligente**

- ✅ **Formats supportés** : PDF, JPEG, PNG
- ✅ **PDF complexes** : Multi-colonnes, tables, images
- ✅ **OCR avancé** : Français, Anglais, Arabe
- ✅ **NLP** : Soft skills automatiques
- ✅ **2795 compétences** en français

**Exemple :**
```json
{
  "nom_complet": "Marie Dupont",
  "email": "marie.dupont@email.com",
  "telephone": "+33 6 12 34 56 78",
  "ville": "Paris",
  "competences_extraites": [
    "Python",
    "Apprentissage Automatique",
    "Analyse de Données",
    "Gestion de Projet",
    "Communication"
  ]
}
```

### **2. Base de Compétences Multi-domaines**

| Domaine | Compétences |
|---------|-------------|
| **IT & Tech** | Python, JavaScript, SQL, Machine Learning, Cloud... |
| **Data Science** | Analyse de Données, Big Data, IA, NLP... |
| **Finance** | Comptabilité, Analyse Financière, Budget, SAP... |
| **Marketing** | Marketing Digital, SEO, Réseaux Sociaux... |
| **RH** | Recrutement, Gestion d'Équipe, Formation... |
| **Soft Skills** | Communication, Leadership, Gestion du Temps... |

**Total :** 2795 compétences (2410 techniques + 385 soft skills)

### **3. Authentification & Gestion Utilisateurs**

- ✅ Inscription / Connexion
- ✅ JWT Token
- ✅ Profil utilisateur
- ✅ Upload photo de profil
- ✅ Préférences d'emploi

### **4. Gestion des CV**

- ✅ Upload multiple
- ✅ Extraction automatique
- ✅ Modification des données
- ✅ Historique des CV

### **5. Offres d'Emploi**

- ✅ Scraping automatique (Rekrute.com)
- ✅ Recherche par compétences
- ✅ Matching CV/Offre
- ✅ Recommandations personnalisées

---

## 🏗️ Architecture

### **Stack Technique**

**Frontend :**
- Next.js 16
- React 19
- TailwindCSS
- shadcn/ui

**Backend :**
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication

**IA & Data :**
- CV Extractor V3
- pdfplumber (extraction PDF)
- Tesseract OCR
- Fuzzy matching (rapidfuzz)
- Dataset 9544 CV réels

### **Structure du Projet**

```
SmartHire/
├── backend/
│   ├── app/
│   │   ├── api/           # Endpoints (auth, users, cvs, offers)
│   │   ├── services/      # CV Extractor V3, Loader
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── core/          # Security, dependencies
│   ├── data/
│   │   ├── resume_skills_complete_fr.json  # 2795 skills FR ✅
│   │   └── resume_data.csv                 # Source (9544 CV)
│   ├── parse_resume_data.py                # Parser principal
│   └── translate_skills_to_french.py       # Traducteur EN→FR
├── app/                   # Frontend Next.js
│   ├── dashboard/         # Pages dashboard
│   ├── auth/             # Authentification
│   └── ...
├── components/           # Components React
├── contexts/            # AuthContext
└── Documentation/
```

---

## 📊 Dataset de Compétences

### **Source**

- **Fichier** : `resume_data.csv` (Kaggle)
- **CV analysés** : 9544
- **Domaines** : Tous secteurs
- **Langue** : Français 🇫🇷

### **Statistiques**

| Métrique | Valeur |
|----------|--------|
| **Compétences totales** | 2795 |
| **Techniques** | 2410 |
| **Soft skills** | 385 |
| **Traductions** | 587 |
| **Fichier principal** | `resume_skills_complete_fr.json` |

### **Top 10 Compétences**

1. Python (3640 occurrences)
2. Apprentissage Automatique (3444)
3. SQL (1736)
4. Analyse de Données (1568)
5. Apprentissage Profond (1512)
6. Excel (1494)
7. Java (1204)
8. C++ (1148)
9. Traitement du Langage Naturel (1092)
10. Ventes (1068)

---

## 🔧 Configuration

### **Backend**

**1. Base de données PostgreSQL**

```env
# backend/.env
DATABASE_URL=postgresql://postgres:ranyaa@localhost:5432/smarthire
SECRET_KEY=your-secret-key-here
```

**2. Dépendances**

```bash
cd backend
pip install -r requirements.txt
```

**Principales :**
- fastapi, uvicorn
- sqlalchemy, psycopg2-binary
- pdfplumber, pytesseract
- rapidfuzz, python-dateutil
- langdetect, pandas

**3. Initialiser la DB**

```bash
# Créer les tables
python -c "from app.database import engine, Base; from app.models import user, cv; Base.metadata.create_all(bind=engine)"
```

### **Frontend**

**1. Dépendances**

```bash
npm install --legacy-peer-deps
```

**2. Variables d'environnement**

```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8080
```

---

## 📖 API Endpoints

### **Authentification**

```http
POST /api/auth/register   # Inscription
POST /api/auth/login      # Connexion
GET  /api/auth/me         # Profil actuel
```

### **CV**

```http
POST   /api/cvs/upload           # Upload CV
GET    /api/cvs                  # Liste CV
GET    /api/cvs/{id}            # Détails CV
PUT    /api/cvs/{id}/update-data # Modifier données
DELETE /api/cvs/{id}            # Supprimer
```

### **Offres**

```http
GET  /api/offers              # Liste offres
GET  /api/offers/search       # Recherche
POST /api/offers/scrape       # Scraper nouvelles offres
```

### **Utilisateurs**

```http
PUT  /api/users/profile           # Mettre à jour profil
POST /api/users/profile-photo     # Upload photo
```

---

## 🎯 Utilisation

### **1. Upload d'un CV**

**Via l'interface :**
1. Se connecter
2. Aller sur Dashboard
3. Cliquer "Upload CV"
4. Sélectionner PDF/Image
5. Les données sont extraites automatiquement

**Via l'API :**
```bash
curl -X POST "http://localhost:8080/api/cvs/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@cv.pdf"
```

### **2. Recherche d'Offres**

**Critères disponibles :**
- Titre du poste
- Ville
- Type de contrat
- Compétences requises
- Salaire minimum

### **3. Matching CV/Offre**

Le système compare automatiquement :
- Compétences du CV
- Compétences requises par l'offre
- Retourne un score de matching (%)

---

## 🧹 Fichiers Conservés (Essentiels)

Après nettoyage, seuls les fichiers essentiels sont conservés :

### **Parser & Traducteur**
- ✅ `parse_resume_data.py` - Parser principal
- ✅ `translate_skills_to_french.py` - Traducteur

### **Extracteur**
- ✅ `cv_extractor_v3.py` - Version finale

### **Datasets**
- ✅ `resume_skills_complete_fr.json` - Principal (FR)
- ✅ `resume_skills_complete.json` - Backup (EN)
- ✅ `resume_data.csv` - Source

### **Documentation**
- ✅ `COMPETENCES_FRANCAIS.md` - Guide compétences
- ✅ `DATASET_RESUME_MULTIDOMAINE.md` - Guide dataset
- ✅ `PROJET_NETTOYE.md` - Nettoyage
- ✅ `CV_EXTRACTOR_V3_ROADMAP.md` - Roadmap V3

---

## 🔄 Maintenance

### **Mettre à jour les compétences**

```bash
cd backend

# 1. Obtenir nouveau dataset CSV avec colonne "skills"
# 2. Placer dans data/resume_data.csv

# 3. Parser
python parse_resume_data.py

# 4. Traduire
python translate_skills_to_french.py

# 5. Redémarrer le serveur
```

### **Ajouter une traduction**

Éditer `translate_skills_to_french.py` :

```python
TRANSLATIONS = {
    'New Skill': 'Nouvelle Compétence',
    ...
}
```

---

## 🆘 Dépannage

### **Serveur ne démarre pas**

```bash
# Vérifier qu'on est dans le bon dossier
cd backend

# Vérifier les dépendances
pip install -r requirements.txt

# Démarrer avec logs
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### **Dataset non trouvé**

```bash
# Vérifier les fichiers
dir backend\data\resume_skills_complete_fr.json

# Si absent, régénérer
cd backend
python parse_resume_data.py
python translate_skills_to_french.py
```

### **Extraction de CV échoue**

- Vérifier que Tesseract est installé
- Vérifier le format du fichier (PDF/JPEG/PNG)
- Vérifier la taille (<10 MB)

---

## 📊 Performance

| Métrique | Valeur |
|----------|--------|
| **Chargement serveur** | ~3 secondes |
| **Extraction CV PDF** | 2-5 secondes |
| **Extraction CV Image** | 3-8 secondes (OCR) |
| **Recherche offres** | <1 seconde |
| **Matching CV/Offre** | <500ms |

---

## 🎉 Résultat

SmartHire est maintenant :

✅ **Fonctionnel** - Toutes les fonctionnalités implémentées  
✅ **Propre** - Code nettoyé, pas de fichiers obsolètes  
✅ **Performant** - Extraction rapide, API optimisée  
✅ **Français** - 2795 compétences traduites  
✅ **Multi-domaines** - IT, Finance, Marketing, RH, Santé...  
✅ **Production-Ready** - Prêt pour déploiement  

---

## 🔗 Liens

- **GitHub** : https://github.com/ranyaserraj/SmartHire.git
- **API Docs** : http://localhost:8080/docs
- **Frontend** : http://localhost:3000

---

## 📝 License

MIT License - Libre d'utilisation

---

**Développé avec ❤️ pour le recrutement intelligent**

