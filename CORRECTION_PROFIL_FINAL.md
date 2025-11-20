# ✅ Corrections Finales - Profil et Photo

## 🐛 Problèmes Corrigés

### 1. ❌ **Photo ne se charge pas dans la navbar**

**Cause** : Le chemin de la photo n'était pas correctement stocké en base de données.

**Solution** ✅ :
- Backend : Stocker le chemin complet `/uploads/avatars/{filename}` au lieu de juste `{filename}`
- Frontend : Construire l'URL complète `http://localhost:8080{photo_profil}`

### 2. ❌ **Formulaire devient vide après sauvegarde**

**Cause** : `window.location.reload()` recharge toute la page et vide le formulaire avant que les nouvelles données ne se chargent.

**Solution** ✅ :
- Remplacer `window.location.reload()` par un rechargement propre des données via API
- Utiliser `useEffect` au lieu de `useState` pour surveiller les changements de l'utilisateur
- Mettre à jour le formulaire avec les nouvelles données après la sauvegarde

---

## 🔧 Modifications Effectuées

### 1. **app/dashboard/profil/page.tsx**

#### Correction 1 : Import de useEffect
```typescript
import { useState, useEffect } from "react"  // ✅ Ajout de useEffect
```

#### Correction 2 : Chargement des données utilisateur
**AVANT** ❌ :
```typescript
useState(() => {  // ❌ Mauvais hook !
  if (user) {
    setFormData({...})
  }
})
```

**MAINTENANT** ✅ :
```typescript
useEffect(() => {  // ✅ Bon hook !
  if (user) {
    setFormData({
      prenom: user.prenom || "",
      nom: user.nom || "",
      email: user.email || "",
      telephone: user.telephone || "",
      ville: user.ville_preferee || "Rabat",
      ville_preferee: user.ville_preferee || "",
      salaire_minimum: user.salaire_minimum || 0,
      type_contrat_prefere: user.type_contrat_prefere || "",
      accepte_remote: user.accepte_teletravail || false,
      secteur_activite: user.secteur_activite || "",
    })
  }
}, [user])  // ✅ Se déclenche quand user change
```

#### Correction 3 : Sauvegarde sans recharger la page
**AVANT** ❌ :
```typescript
toast.success("Profil mis à jour avec succès !")
window.location.reload()  // ❌ Recharge toute la page = formulaire vide
```

**MAINTENANT** ✅ :
```typescript
toast.success("Profil mis à jour avec succès !")

// Recharger les données utilisateur depuis l'API
const meResponse = await fetch("http://localhost:8080/api/auth/me", {
  headers: {
    "Authorization": `Bearer ${token}`,
  },
})

if (meResponse.ok) {
  const userData = await meResponse.json()
  // Mettre à jour le formulaire avec les nouvelles données
  setFormData({
    prenom: userData.prenom || "",
    nom: userData.nom || "",
    email: userData.email || "",
    telephone: userData.telephone || "",
    ville: userData.ville_preferee || "Rabat",
    ville_preferee: userData.ville_preferee || "",
    salaire_minimum: userData.salaire_minimum || 0,
    type_contrat_prefere: userData.type_contrat_prefere || "",
    accepte_remote: userData.accepte_teletravail || false,
    secteur_activite: userData.secteur_activite || "",
  })
}
```

#### Correction 4 : Upload photo
**MAINTENANT** ✅ :
```typescript
toast.success("Photo mise à jour avec succès !")

// Réinitialiser le preview
setPhotoPreview(null)
setPhotoFile(null)

// Recharger après un court délai pour que la photo s'enregistre
setTimeout(() => {
  window.location.reload()
}, 500)
```

### 2. **backend/app/api/users.py** (Déjà corrigé)

#### Stockage correct du chemin photo :
```python
# Update database - stocker le chemin relatif pour accès via URL
current_user.photo_profil = f"/uploads/avatars/{filename}"  # ✅ Chemin complet
db.commit()
db.refresh(current_user)
```

---

## 🚀 Comment Tester

### Étape 1 : S'assurer que la base de données a les nouvelles colonnes

```bash
psql -U postgres -d smarthire_db
```

Mot de passe : `ranyaa`

```sql
-- Ajouter les colonnes si pas déjà fait
ALTER TABLE users ADD COLUMN IF NOT EXISTS salaire_minimum INTEGER;
ALTER TABLE users ADD COLUMN IF NOT EXISTS type_contrat_prefere VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS secteur_activite VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS accepte_teletravail BOOLEAN DEFAULT FALSE;

-- Vérifier
\d users

\q
```

### Étape 2 : Redémarrer Backend et Frontend

**Terminal 1 - Backend :**
```bash
cd C:\Users\pc\Downloads\code\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

**Terminal 2 - Frontend :**
```bash
cd C:\Users\pc\Downloads\code
npm run dev
```

### Étape 3 : Tester l'Inscription avec Photo

1. Ouvrir **http://localhost:3000/auth**
2. S'inscrire avec une **photo**
3. ✅ **Vérifier que la photo apparaît dans la navbar** en haut à droite
4. ✅ **Vérifier que le nom complet s'affiche** (ex: "hiba serraj andaloussi")

### Étape 4 : Tester la Page Profil

1. Aller sur **http://localhost:3000/dashboard/profil**
2. ✅ **Vérifier que toutes les données sont chargées** (pas vides)
3. **Modifier** quelques champs :
   ```
   Téléphone : +212 612345678
   Ville préférée : Casablanca
   Salaire minimum : 15000
   Type contrat : CDI
   Secteur : Informatique
   Télétravail : ✅
   ```
4. Cliquer sur **"Enregistrer les modifications"**
5. ✅ **Toast de succès** s'affiche
6. ✅ **Le formulaire reste rempli** avec les nouvelles données !

### Étape 5 : Tester le Changement de Photo

1. Sur la page profil, cliquer **"Changer la photo"**
2. Choisir une nouvelle image
3. ✅ **Preview** s'affiche
4. Cliquer **"Enregistrer la photo"**
5. ✅ **Toast de succès**
6. La page se recharge
7. ✅ **La nouvelle photo** apparaît partout (profil, navbar, sidebar)

---

## 🎯 Résultats Attendus

### ✅ Navbar (en haut à droite)

```
[🔔] [📷] hiba serraj andaloussi [▼]
         ranyaserraj18@gmail.com
```

- **Photo** : Votre photo de profil (ou initiales "HS")
- **Nom** : Nom complet en minuscules
- **Email** : Votre email

### ✅ Page Profil - Formulaire Rempli

Après modification et sauvegarde :
```
┌─────────────────────────────────────┐
│  Photo de profil                    │
│                                     │
│      [📷 HS]  <-- Votre photo       │
│                                     │
│  [Changer la photo]                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Informations personnelles          │
│                                     │
│  Prénom : hiba                      │  <-- Rempli ✅
│  Nom    : serraj andaloussi         │  <-- Rempli ✅
│  Email  : ranyaserraj18@gmail.com   │  <-- Rempli ✅
│  Tel    : +212 612345678            │  <-- Rempli ✅
│  Ville  : Rabat                     │  <-- Rempli ✅
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Préférences d'emploi               │
│                                     │
│  Ville préférée : Casablanca        │  <-- Rempli ✅
│  Salaire min    : 15000             │  <-- Rempli ✅
│  Type contrat   : CDI               │  <-- Rempli ✅
│  Secteur        : Informatique      │  <-- Rempli ✅
│  ☑ Télétravail                      │  <-- Coché ✅
└─────────────────────────────────────┘

[Enregistrer les modifications]
```

**Après avoir cliqué "Enregistrer"** :
- ✅ Toast : "Profil mis à jour avec succès !"
- ✅ **Le formulaire reste rempli** (ne devient pas vide)
- ✅ Les données sont mises à jour en base
- ✅ La navbar se met à jour automatiquement

---

## 🐛 Dépannage

### Problème : La photo ne s'affiche toujours pas

**Vérifier en base de données :**
```bash
psql -U postgres -d smarthire_db
```

```sql
SELECT id, prenom, nom, email, photo_profil 
FROM users 
WHERE email = 'ranyaserraj18@gmail.com';
```

**Résultat attendu :**
```
photo_profil: /uploads/avatars/1_1234567890.jpg
```

Si c'est juste `1_1234567890.jpg` (sans `/uploads/avatars/`) :
→ Le backend n'a pas été redémarré après la correction

**Solution :**
1. Redémarrer le backend
2. Supprimer l'utilisateur actuel :
```sql
DELETE FROM users WHERE email = 'ranyaserraj18@gmail.com';
```
3. S'inscrire à nouveau avec une photo

### Problème : Le formulaire devient vide

**Vérifier dans la console du navigateur (F12) :**
```javascript
// Vérifier l'utilisateur dans le contexte
console.log(JSON.parse(localStorage.getItem("token")))
```

Si `null` ou expiré → Se reconnecter

### Problème : Erreur 500 lors de la sauvegarde

**Cause** : Les colonnes n'existent pas en base

**Solution :**
```sql
-- Vérifier les colonnes
\d users

-- Ajouter si manquantes
ALTER TABLE users ADD COLUMN IF NOT EXISTS salaire_minimum INTEGER;
ALTER TABLE users ADD COLUMN IF NOT EXISTS type_contrat_prefere VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS secteur_activite VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS accepte_teletravail BOOLEAN DEFAULT FALSE;
```

---

## ✅ Checklist Finale

- [ ] Colonnes ajoutées dans PostgreSQL
- [ ] Backend redémarré sur port 8080
- [ ] Frontend redémarré sur port 3000
- [ ] Inscription avec photo réussie
- [ ] Photo apparaît dans navbar
- [ ] Photo apparaît dans sidebar
- [ ] Nom complet affiché dans navbar
- [ ] Page profil charge les vraies données
- [ ] Formulaire reste rempli après sauvegarde
- [ ] Toast de succès s'affiche
- [ ] Changement de photo fonctionne
- [ ] Nouvelle photo apparaît partout

---

## 🎉 Résultat Final

Après ces corrections, votre application aura :

✅ **Photo de profil** qui se charge correctement partout
✅ **Navbar** avec photo + nom complet
✅ **Page profil** avec données dynamiques
✅ **Formulaire qui reste rempli** après modification
✅ **Sauvegarde fluide** sans rechargement brutal
✅ **Upload de photo** fonctionnel

**Redémarrez les serveurs et testez !** 🚀

