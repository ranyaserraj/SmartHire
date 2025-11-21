# 🔧 Correction de l'Authentification - Guide Complet

## 🎯 Symptôme

L'authentification ne fonctionne pas : impossible de se connecter ou de s'inscrire.

## 🔍 Diagnostic Rapide

### Étape 1 : Vérifier que le Backend est Démarré

```bash
# Vérifier si le serveur répond
curl http://localhost:8080/docs
```

**Si ça ne fonctionne pas :**
```bash
cd C:\Users\pc\Downloads\code\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Étape 2 : Tester l'API Backend

```bash
cd backend
python test_auth.py
```

Ce script teste automatiquement :
- ✅ Connexion au serveur
- ✅ Inscription d'un utilisateur
- ✅ Connexion avec mot de passe
- ✅ Récupération du profil

### Étape 3 : Vérifier le Frontend

```bash
cd C:\Users\pc\Downloads\code
npm run dev
```

Le frontend doit être accessible sur `http://localhost:3000`

## 🐛 Problèmes Courants et Solutions

### ❌ Problème 1 : "ModuleNotFoundError: No module named 'pdfplumber'"

**Cause :** Les dépendances du CV Extractor V2 ne sont pas installées.

**Solution :**
```bash
cd backend
pip install pdfplumber rapidfuzz python-dateutil
```

Puis redémarrer le serveur (Ctrl+C puis relancer).

### ❌ Problème 2 : "Connection refused" ou "ECONNREFUSED"

**Cause :** Le backend n'est pas en cours d'exécution.

**Solution :**
```bash
cd C:\Users\pc\Downloads\code\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

**Vérifier que vous voyez :**
```
INFO:     Application startup complete.
==================================================
🚀 SmartHire API Started
==================================================
📚 Documentation: http://localhost:8080/docs
```

### ❌ Problème 3 : "Email ou mot de passe incorrect"

**Causes possibles :**
1. Mauvais identifiants
2. Utilisateur pas encore enregistré
3. Erreur de hash du mot de passe

**Solution :**
```bash
# 1. Tester avec le script
cd backend
python test_auth.py

# 2. Si ça fonctionne, le problème est côté frontend
# 3. Vérifier la console du navigateur (F12)
```

### ❌ Problème 4 : CORS Error

**Erreur dans la console :**
```
Access to fetch at 'http://localhost:8080/api/auth/login' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution :** Vérifier `backend/app/main.py` :

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### ❌ Problème 5 : "Unauthorized" ou Token Invalide

**Cause :** JWT mal configuré ou expiré.

**Solution :**

1. **Vérifier `.env` dans `backend/` :**
```bash
# backend/.env
SECRET_KEY=votre-secret-key-très-sécurisée-changez-moi
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

2. **Régénérer une nouvelle SECRET_KEY :**
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

3. **Mettre à jour `.env` avec la nouvelle clé**

4. **Redémarrer le serveur**

### ❌ Problème 6 : Database Connection Error

**Erreur :**
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```

**Solution :**

1. **Vérifier que PostgreSQL est démarré**
2. **Vérifier `.env` :**
```bash
DATABASE_URL=postgresql://postgres:ranyaa@localhost:5432/smarthire_db
```

3. **Tester la connexion :**
```bash
psql -U postgres -d smarthire_db
# Mot de passe : ranyaa
```

## 📋 Checklist Complète

### Backend ✅

- [ ] PostgreSQL est démarré
- [ ] Database `smarthire_db` existe
- [ ] Fichier `.env` correctement configuré
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] **Nouvelles dépendances V2 installées** (`pip install pdfplumber rapidfuzz python-dateutil`)
- [ ] Serveur backend en cours d'exécution sur port 8080
- [ ] `http://localhost:8080/docs` accessible
- [ ] Test `python test_auth.py` réussi

### Frontend ✅

- [ ] Dépendances installées (`npm install`)
- [ ] Serveur frontend en cours d'exécution (`npm run dev`)
- [ ] `http://localhost:3000` accessible
- [ ] `AuthContext.tsx` avec `USE_MOCK_AUTH = false`
- [ ] URLs dans `AuthContext.tsx` pointent vers `http://localhost:8080`

## 🧪 Tests Manuels

### Test 1 : Inscription via l'Interface

1. Aller sur `http://localhost:3000/auth`
2. Cliquer sur l'onglet "S'inscrire"
3. Remplir le formulaire :
   - Prénom : Test
   - Nom : User
   - Email : test@example.com
   - Mot de passe : test123456
   - Confirmer : test123456
4. Cliquer sur "Créer mon compte"

**Résultat attendu :** Redirection vers `/dashboard` avec message "Inscription réussie !"

### Test 2 : Connexion via l'Interface

1. Aller sur `http://localhost:3000/auth`
2. Onglet "Connexion"
3. Entrer :
   - Email : test@example.com
   - Mot de passe : test123456
4. Cliquer sur "Se connecter"

**Résultat attendu :** Redirection vers `/dashboard` avec message "Connexion réussie !"

### Test 3 : Vérifier la Session

1. Une fois connecté, aller sur `/dashboard/profil`
2. Vérifier que vos informations s'affichent
3. Ouvrir la console du navigateur (F12)
4. Taper : `localStorage.getItem("token")`

**Résultat attendu :** Un token JWT s'affiche

## 🔧 Debug Avancé

### Vérifier les Logs Backend

Regarder le terminal où le serveur backend tourne. Vous devriez voir :

```
INFO:     127.0.0.1:xxxxx - "POST /api/auth/register HTTP/1.1" 201 Created
INFO:     127.0.0.1:xxxxx - "POST /api/auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "GET /api/auth/me HTTP/1.1" 200 OK
```

### Vérifier les Logs Frontend

Ouvrir la console du navigateur (F12) et regarder :

1. **Onglet Console :** Erreurs JavaScript
2. **Onglet Network :** Requêtes HTTP
   - Filtrer par "XHR" ou "Fetch"
   - Regarder les requêtes vers `localhost:8080`
   - Vérifier les status codes (200 = OK, 401 = Unauthorized, etc.)

### Tester l'API avec curl

```bash
# Test registration
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "curl@test.com",
    "mot_de_passe": "test123456",
    "nom": "Test",
    "prenom": "Curl"
  }'

# Test login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "curl@test.com",
    "mot_de_passe": "test123456"
  }'

# Test get user (remplacer TOKEN par le token reçu)
curl -X GET http://localhost:8080/api/auth/me \
  -H "Authorization: Bearer TOKEN"
```

## 🆘 Si Rien ne Fonctionne

### Reset Complet

```bash
# 1. Arrêter tous les serveurs (Ctrl+C)

# 2. Réinstaller les dépendances backend
cd backend
pip install --upgrade -r requirements.txt
pip install pdfplumber rapidfuzz python-dateutil

# 3. Réinstaller les dépendances frontend
cd ..
npm install

# 4. Reset la base de données
psql -U postgres
DROP DATABASE smarthire_db;
CREATE DATABASE smarthire_db;
\q

# 5. Relancer le backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# 6. Dans un autre terminal, relancer le frontend
cd ..
npm run dev

# 7. Tester l'inscription
```

## 📞 Support

Si après toutes ces étapes ça ne fonctionne toujours pas :

1. **Copier les erreurs exactes** du terminal backend
2. **Copier les erreurs** de la console du navigateur (F12)
3. **Exécuter** `python backend/test_auth.py` et copier le résultat
4. **Fournir ces informations** pour un diagnostic précis

---

**Version :** 1.0  
**Dernière mise à jour :** 21/11/2024  
**Pour :** SmartHire Authentication System

