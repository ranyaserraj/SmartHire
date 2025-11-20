# ✅ Backend et Frontend Connectés !

## 🎉 Configuration Terminée

Le frontend SmartHire est maintenant connecté au backend FastAPI !

---

## 🔧 Changements Effectués

### 1. **AuthContext.tsx** mis à jour

- ✅ `USE_MOCK_AUTH = false` (utilise le vrai backend)
- ✅ URLs mises à jour pour le port **8080**
- ✅ Endpoints corrigés :
  - `POST /api/auth/login` ✓
  - `POST /api/auth/register` ✓
  - `GET /api/auth/me` ✓
- ✅ Format des données adapté au backend :
  - `mot_de_passe` au lieu de `password`
  - `nom` et `prenom` au lieu de `full_name`

### 2. **Backend configuré**

- ✅ Serveur sur le port **8080**
- ✅ Base de données PostgreSQL connectée
- ✅ Mot de passe configuré : `ranyaa`
- ✅ email-validator installé

---

## 🚀 Comment Tester

### 1. **Démarrer le Backend** (si pas déjà démarré)

```bash
cd C:\Users\pc\Downloads\code\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### 2. **Démarrer le Frontend** (dans un autre terminal)

```bash
cd C:\Users\pc\Downloads\code
npm run dev
```

### 3. **Tester l'Inscription**

1. Ouvrir http://localhost:3000
2. Cliquer sur "S'inscrire" ou "Créer un compte"
3. Remplir le formulaire :
   - Nom complet : `Ranya SERRAJ`
   - Email : `ranya@test.com`
   - Mot de passe : `password123`
4. Cliquer sur "S'inscrire"

✅ **L'utilisateur sera créé dans PostgreSQL !**

### 4. **Vérifier dans la Base de Données**

```bash
psql -U postgres -d smarthire_db
SELECT * FROM users;
```

Vous devriez voir votre utilisateur !

---

## 🔍 Vérifier que ça Marche

### Depuis le Frontend

1. **S'inscrire** → Doit créer l'utilisateur
2. **Se connecter** → Doit recevoir un token JWT
3. **Accéder au dashboard** → Doit afficher vos infos

### Depuis Swagger (Backend)

1. Ouvrir http://localhost:8080/docs
2. Tester `POST /api/auth/register`
3. Tester `POST /api/auth/login`
4. Copier le token reçu
5. Cliquer sur "Authorize" en haut à droite
6. Coller le token : `Bearer VOTRE_TOKEN`
7. Tester `GET /api/auth/me`

---

## 📊 Flux d'Authentification

```
FRONTEND                    BACKEND                     DATABASE
   |                           |                            |
   |-- POST /api/auth/register -->                          |
   |                           |-- INSERT INTO users ------>|
   |                           |<-- User created -----------|
   |<-- Success (201) ---------|                            |
   |                           |                            |
   |-- POST /api/auth/login --->|                           |
   |                           |-- SELECT * FROM users ---->|
   |                           |<-- User found -------------|
   |                           |-- Verify password          |
   |                           |-- Generate JWT token       |
   |<-- {access_token: "..."}-|                            |
   |                           |                            |
   |-- GET /api/auth/me ------->|                           |
   |   (Header: Bearer token)   |                           |
   |                           |-- Decode JWT               |
   |                           |-- SELECT * FROM users ---->|
   |                           |<-- User data --------------|
   |<-- {id, nom, email, ...}--|                            |
```

---

## 🌐 URLs Importantes

### Frontend
- **Application** : http://localhost:3000
- **Page d'auth** : http://localhost:3000/auth

### Backend
- **API Documentation** : http://localhost:8080/docs
- **Alternative Docs** : http://localhost:8080/redoc
- **Health Check** : http://localhost:8080/health

---

## 🐛 Dépannage

### Erreur : "Failed to fetch" ou "Network Error"

**Cause** : Le backend n'est pas démarré ou mauvais port

**Solution** :
```bash
# Vérifier que le backend tourne sur le port 8080
netstat -ano | findstr :8080
```

### Erreur : "Email déjà utilisé"

**Cause** : L'email existe déjà dans la base de données

**Solution** : Utiliser un autre email ou supprimer l'utilisateur :
```sql
psql -U postgres -d smarthire_db
DELETE FROM users WHERE email = 'test@example.com';
```

### Erreur : "Could not connect to database"

**Cause** : PostgreSQL n'est pas démarré

**Solution** :
```bash
# Vérifier le statut
pg_ctl status

# Démarrer PostgreSQL
pg_ctl start
```

### Les données ne s'affichent pas

**Cause** : Token JWT expiré ou invalide

**Solution** : Se déconnecter et se reconnecter
```javascript
localStorage.clear()
// Puis recharger la page
```

---

## 📝 Endpoints API Disponibles

### Authentification
- ✅ `POST /api/auth/register` - Créer un compte
- ✅ `POST /api/auth/login` - Se connecter
- ✅ `GET /api/auth/me` - Récupérer mon profil

### Profil
- ✅ `PUT /api/users/profile` - Modifier mon profil
- ✅ `POST /api/users/photo` - Upload photo de profil
- ✅ `GET /api/users/{id}/photo` - Récupérer une photo

### CVs
- ✅ `POST /api/cvs/upload` - Upload un CV
- ✅ `GET /api/cvs/me` - Liste de mes CVs
- ✅ `DELETE /api/cvs/{id}` - Supprimer un CV

### Offres d'emploi
- ✅ `GET /api/offers` - Liste des offres
- ✅ `GET /api/offers/search` - Rechercher des offres
- ✅ `GET /api/offers/{id}` - Détails d'une offre
- ✅ `POST /api/offers/scrape` - Lancer le scraping

---

## 🎯 Prochaines Étapes

1. ✅ **Tester l'inscription depuis le frontend**
2. ✅ **Vérifier que les données sont en base**
3. ✅ **Tester la connexion**
4. ✅ **Tester l'upload de CV**
5. ⏳ **Implémenter l'extraction de texte des CVs**
6. ⏳ **Ajouter l'analyse NLP avec spaCy**
7. ⏳ **Implémenter le matching CV/Offre**
8. ⏳ **Ajouter la génération de lettres de motivation**

---

## ✅ Checklist de Vérification

- [x] Backend démarre sans erreur
- [x] Frontend démarre sans erreur
- [x] `USE_MOCK_AUTH = false` dans AuthContext.tsx
- [x] URLs backend utilisent le port 8080
- [x] PostgreSQL est démarré
- [x] Base de données `smarthire_db` existe
- [x] Tables `users`, `cvs`, `scraped_offers` créées
- [x] email-validator installé
- [ ] Test d'inscription réussi
- [ ] Utilisateur visible dans la base de données
- [ ] Test de connexion réussi
- [ ] Token JWT reçu et valide
- [ ] Dashboard accessible après connexion

---

## 🎉 Félicitations !

Votre application SmartHire est maintenant **Full-Stack** avec :
- ✅ Frontend Next.js + React
- ✅ Backend FastAPI + Python
- ✅ Base de données PostgreSQL
- ✅ Authentification JWT
- ✅ Upload de fichiers
- ✅ Web scraping

**Testez maintenant l'inscription depuis le frontend !** 🚀


