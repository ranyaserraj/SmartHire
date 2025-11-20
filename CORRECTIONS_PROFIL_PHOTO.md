# ✅ Corrections - Profil et Photo

## 🎯 Problèmes Résolus

1. ✅ **Photo de profil ne se charge pas dans la navbar**
2. ✅ **Informations statiques dans la page profil**
3. ✅ **Champs manquants dans la table users**

---

## 🔧 Modifications Effectuées

### 1. **Base de Données - Nouveaux Champs**

✅ Ajout de 4 nouveaux champs dans la table `users` :

| Champ | Type | Description |
|-------|------|-------------|
| `salaire_minimum` | INTEGER | Salaire minimum souhaité en MAD |
| `type_contrat_prefere` | VARCHAR(50) | CDI, CDD, Stage, Freelance |
| `secteur_activite` | VARCHAR(100) | Secteur d'activité préféré |
| `accepte_teletravail` | BOOLEAN | Accepte le télétravail (true/false) |

### 2. **Backend - Modèles et API**

#### `backend/app/models/user.py` ✅
- Ajout des 4 nouveaux champs au modèle SQLAlchemy

#### `backend/app/schemas/user.py` ✅
- Mise à jour de `UserResponse` pour inclure les nouveaux champs
- Mise à jour de `UserUpdate` pour permettre la modification

#### `backend/app/api/users.py` ✅
- Mise à jour de `PUT /api/users/profile` pour gérer tous les champs
- Correction du stockage de la photo : `/uploads/avatars/{filename}` au lieu de juste `{filename}`

### 3. **Frontend - Page Profil**

#### `app/dashboard/profil/page.tsx` ✅
**AVANT** : Données statiques hardcodées
**MAINTENANT** : Données dynamiques depuis l'utilisateur connecté

**Fonctionnalités ajoutées :**
- ✅ Chargement des vraies données utilisateur depuis `useAuth()`
- ✅ Upload de photo fonctionnel avec preview
- ✅ Enregistrement des modifications vers l'API
- ✅ États de chargement (loading)
- ✅ Gestion d'erreurs complète

### 4. **Frontend - Contexte Auth**

#### `contexts/AuthContext.tsx` ✅
- Ajout des nouveaux champs dans l'interface `User`
- Correction de l'URL de la photo

---

## 🚀 Comment Appliquer les Modifications

### Étape 1 : Ajouter les Colonnes dans PostgreSQL

**Ouvrir un terminal et exécuter :**

```bash
psql -U postgres -d smarthire_db
```

Mot de passe : `ranyaa`

**Puis copier-coller ce script SQL :**

```sql
-- Ajouter les nouvelles colonnes
ALTER TABLE users ADD COLUMN IF NOT EXISTS salaire_minimum INTEGER;
ALTER TABLE users ADD COLUMN IF NOT EXISTS type_contrat_prefere VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS secteur_activite VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS accepte_teletravail BOOLEAN DEFAULT FALSE;

-- Vérifier
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'users'
ORDER BY ordinal_position;

-- Quitter
\q
```

✅ **Vous devriez voir les 4 nouvelles colonnes !**

### Étape 2 : Redémarrer le Backend

**Terminal 1 - Arrêter le backend (Ctrl+C) puis :**

```bash
cd C:\Users\pc\Downloads\code\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

✅ **Attendre le message :**
```
🚀 SmartHire API Started
📚 Documentation: http://localhost:8080/docs
```

### Étape 3 : Redémarrer le Frontend

**Terminal 2 :**

```bash
cd C:\Users\pc\Downloads\code
npm run dev
```

✅ **Attendre :**
```
✓ Ready in 2.5s
○ Local: http://localhost:3000
```

---

## 🧪 Tests à Effectuer

### Test 1 : Vérifier la Photo dans la Navbar

1. Ouvrir **http://localhost:3000/auth**
2. S'inscrire avec une **photo de profil**
3. ✅ **Après inscription**, vérifier que :
   - La photo apparaît dans la **navbar** (en haut à droite)
   - La photo apparaît dans la **sidebar** (en bas)
   - Le **nom complet** s'affiche (ex: "Ranya SERRAJ")

### Test 2 : Page Profil avec Vraies Données

1. Aller sur **http://localhost:3000/dashboard/profil**
2. ✅ **Vérifier que les données affichées sont les vôtres** :
   - Prénom
   - Nom
   - Email
   - Téléphone
   - Ville préférée

### Test 3 : Modifier le Profil

1. Sur la page profil, modifier :
   ```
   Ville préférée : Casablanca
   Salaire minimum : 15000
   Type de contrat : CDI
   Secteur : Informatique
   Télétravail : ✅ (coché)
   ```

2. Cliquer sur **"Enregistrer les modifications"**

3. ✅ **Toast de succès** : "Profil mis à jour avec succès !"

4. Recharger la page → Vérifier que les modifications sont conservées

### Test 4 : Changer la Photo de Profil

1. Sur la page profil, cliquer sur **"Changer la photo"**
2. Choisir une nouvelle image
3. ✅ **Preview** s'affiche
4. Cliquer à nouveau sur **"Enregistrer la photo"**
5. ✅ La photo s'affiche dans l'avatar
6. Aller sur le **Dashboard** → Photo mise à jour partout !

### Test 5 : Vérifier en Base de Données

```bash
psql -U postgres -d smarthire_db
```

```sql
SELECT id, prenom, nom, email, photo_profil, 
       ville_preferee, salaire_minimum, type_contrat_prefere, 
       secteur_activite, accepte_teletravail
FROM users
WHERE email = 'votre_email@test.com';
```

✅ **Vous devriez voir toutes vos données enregistrées !**

---

## 🐛 Résolution des Problèmes

### Problème 1 : La photo ne s'affiche toujours pas

**Cause** : La photo n'a pas le bon chemin

**Solution :**
1. Ouvrir la console du navigateur (F12)
2. Regarder l'URL de l'image qui est chargée
3. Vérifier que ça commence par `http://localhost:8080/uploads/avatars/`

**Vérifier en base :**
```sql
SELECT photo_profil FROM users WHERE id = 1;
```

Devrait retourner : `/uploads/avatars/1_1234567890.jpg`

### Problème 2 : Erreur 500 lors de la sauvegarde

**Cause** : Les colonnes n'existent pas encore en base

**Solution :**
```bash
psql -U postgres -d smarthire_db
```

```sql
-- Vérifier si les colonnes existent
\d users

-- Si non, les ajouter
ALTER TABLE users ADD COLUMN IF NOT EXISTS salaire_minimum INTEGER;
ALTER TABLE users ADD COLUMN IF NOT EXISTS type_contrat_prefere VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS secteur_activite VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS accepte_teletravail BOOLEAN DEFAULT FALSE;
```

### Problème 3 : Les données ne se chargent pas

**Cause** : L'utilisateur n'est pas connecté

**Solution :**
1. Se déconnecter
2. Se reconnecter
3. Vérifier que le token est valide dans `localStorage`

**Dans la console du navigateur :**
```javascript
console.log(localStorage.getItem("token"))
```

Si `null` → Problème de connexion

### Problème 4 : Photo trop grande

**Erreur** : "La photo ne doit pas dépasser 5MB"

**Solution** : Réduire la taille de l'image avant de l'uploader

---

## 📊 Structure Complète de la Table Users

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    telephone VARCHAR(20),
    photo_profil VARCHAR(255),
    ville_preferee VARCHAR(100),
    
    -- Nouveaux champs
    salaire_minimum INTEGER,
    type_contrat_prefere VARCHAR(50),
    secteur_activite VARCHAR(100),
    accepte_teletravail BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🎨 Capture d'Écran Attendue

### Navbar (en haut à droite)

```
┌─────────────────────────────────────┐
│  🔔  [📷] Ranya SERRAJ [▼]         │
│          ranya@test.com             │
└─────────────────────────────────────┘
```

### Page Profil

```
┌────────────────────────────────────────────────┐
│  Mon Profil                                    │
├────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────────────────┐│
│  │ Photo       │  │ Informations             ││
│  │             │  │                          ││
│  │   [📷 RS]   │  │ Prénom : Ranya           ││
│  │             │  │ Nom    : SERRAJ          ││
│  │ [Changer]   │  │ Email  : ranya@test.com  ││
│  └─────────────┘  │ Tel    : +212 6XX...     ││
│                   │ Ville  : Rabat           ││
│                   └──────────────────────────┘│
│                                                │
│  ┌────────────────────────────────────────────┐│
│  │ Préférences d'emploi                       ││
│  │                                            ││
│  │ Ville préférée : Casablanca                ││
│  │ Salaire min    : 12000 MAD                 ││
│  │ Type contrat   : CDI                       ││
│  │ Secteur        : Informatique              ││
│  │ ☑ J'accepte le télétravail                ││
│  └────────────────────────────────────────────┘│
│                                                │
│                    [Enregistrer modifications] │
└────────────────────────────────────────────────┘
```

---

## ✅ Checklist Finale

- [ ] Colonnes ajoutées dans PostgreSQL
- [ ] Backend redémarré sans erreur
- [ ] Frontend redémarré sans erreur
- [ ] Photo s'affiche dans navbar
- [ ] Photo s'affiche dans sidebar
- [ ] Nom complet affiché correctement
- [ ] Page profil charge les vraies données
- [ ] Modification du profil fonctionne
- [ ] Upload de photo fonctionne
- [ ] Toast de succès s'affiche
- [ ] Données enregistrées en base

---

## 🎉 Résultat Final

Après ces corrections, votre application SmartHire aura :

✅ **Photo de profil fonctionnelle** partout (navbar, sidebar, profil)
✅ **Page profil dynamique** avec vraies données utilisateur
✅ **Préférences d'emploi complètes** enregistrées en base
✅ **Modification du profil** fonctionnelle
✅ **Upload de photo** fonctionnel
✅ **Persistance des données** garantie

**Testez maintenant !** 🚀

