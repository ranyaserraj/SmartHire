# ✅ Solution - Préférences d'emploi ne s'affichent pas

## 🐛 Problèmes

1. ❌ **Les préférences d'emploi ne s'affichent pas** quand on revient sur la page profil
2. ❌ **Pas de redirection** vers le dashboard après la sauvegarde

---

## 🔧 Corrections Effectuées

### 1. **Chargement des Données avec Logs**

Ajout de `console.log` pour déboguer :

```typescript
useEffect(() => {
  console.log("User data:", user)  // ✅ Pour vérifier les données
  
  if (user) {
    setFormData({
      prenom: user.prenom || "",
      nom: user.nom || "",
      email: user.email || "",
      telephone: user.telephone || "",
      ville: user.ville_preferee || "",
      ville_preferee: user.ville_preferee || "",
      salaire_minimum: user.salaire_minimum || 0,  // ✅ Important !
      type_contrat_prefere: user.type_contrat_prefere || "",  // ✅ Important !
      accepte_remote: user.accepte_teletravail || false,  // ✅ Important !
      secteur_activite: user.secteur_activite || "",  // ✅ Important !
    })
    setIsLoading(false)
  }
}, [user])
```

### 2. **Redirection vers Dashboard après Sauvegarde**

```typescript
const handleSave = async () => {
  // ... sauvegarde ...
  
  toast.success("Profil mis à jour avec succès !")
  
  // Recharger les données
  const meResponse = await fetch("http://localhost:8080/api/auth/me", {
    headers: { "Authorization": `Bearer ${token}` }
  })
  
  if (meResponse.ok) {
    const userData = await meResponse.json()
    console.log("Données rechargées:", userData)
    
    // ✅ Rediriger vers le dashboard après 1 seconde
    setTimeout(() => {
      router.push("/dashboard")
    }, 1000)
  }
}
```

---

## 🚀 Tests à Faire

### Test 1 : Vérifier les Données en Base

**Ouvrir un terminal PowerShell :**

```bash
psql -U postgres -d smarthire_db
```

Mot de passe : `ranyaa`

**Exécuter cette requête :**

```sql
SELECT 
    id,
    prenom,
    nom,
    email,
    ville_preferee,
    salaire_minimum,
    type_contrat_prefere,
    secteur_activite,
    accepte_teletravail
FROM users
WHERE email = 'hind@gmail.com';  -- Remplacer par votre email
```

✅ **Résultat attendu :**
```
 id | prenom | nom           | email          | ville_preferee | salaire_minimum | type_contrat_prefere | secteur_activite | accepte_teletravail
----+--------+---------------+----------------+----------------+-----------------+----------------------+------------------+---------------------
  1 | hind   | iraqi houssaini| hind@gmail.com | Fès            | 0               |                      |                  | f
```

**Si les colonnes sont `null` ou vides** → Les données ne sont pas enregistrées !

### Test 2 : Vérifier que les Colonnes Existent

```sql
\d users
```

Vous devriez voir :
```
salaire_minimum        | integer
type_contrat_prefere   | character varying(50)
secteur_activite       | character varying(100)
accepte_teletravail    | boolean
```

**Si ces colonnes n'existent pas** :

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS salaire_minimum INTEGER;
ALTER TABLE users ADD COLUMN IF NOT EXISTS type_contrat_prefere VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS secteur_activite VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS accepte_teletravail BOOLEAN DEFAULT FALSE;
```

### Test 3 : Tester l'API Backend

**Ouvrir la console du navigateur (F12) et exécuter :**

```javascript
const token = localStorage.getItem("token")

// Test 1: Récupérer les données utilisateur
fetch("http://localhost:8080/api/auth/me", {
  headers: { "Authorization": `Bearer ${token}` }
})
  .then(r => r.json())
  .then(data => console.log("User data:", data))

// Test 2: Mettre à jour le profil
fetch("http://localhost:8080/api/users/profile", {
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify({
    salaire_minimum: 15000,
    type_contrat_prefere: "CDI",
    secteur_activite: "Informatique",
    accepte_teletravail: true
  })
})
  .then(r => r.json())
  .then(data => console.log("Updated user:", data))
```

### Test 4 : Test Complet Frontend

1. **Ouvrir** http://localhost:3000/dashboard/profil
2. **Ouvrir la console** (F12)
3. **Vérifier le log** : `User data: { ... }`
4. **Remplir les préférences** :
   ```
   Ville préférée : Casablanca
   Salaire minimum : 15000
   Type contrat : CDI
   Secteur : Informatique
   ☑ Télétravail
   ```
5. **Cliquer** "Enregistrer les modifications"
6. ✅ **Toast de succès**
7. ✅ **Redirection vers /dashboard** après 1 seconde
8. **Retourner sur** http://localhost:3000/dashboard/profil
9. ✅ **Les données doivent être là !**

---

## 🐛 Si les Données ne s'Affichent Pas

### Problème 1 : Colonnes n'existent pas

**Vérifier :**
```sql
\d users
```

**Ajouter si manquantes :**
```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS salaire_minimum INTEGER;
ALTER TABLE users ADD COLUMN IF NOT EXISTS type_contrat_prefere VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS secteur_activite VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS accepte_teletravail BOOLEAN DEFAULT FALSE;
```

### Problème 2 : Backend ne retourne pas les nouveaux champs

**Vérifier dans** `backend/app/schemas/user.py` :

```python
class UserResponse(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    telephone: Optional[str] = None
    photo_profil: Optional[str] = None
    ville_preferee: Optional[str] = None
    salaire_minimum: Optional[int] = None  # ✅ Doit être là
    type_contrat_prefere: Optional[str] = None  # ✅ Doit être là
    secteur_activite: Optional[str] = None  # ✅ Doit être là
    accepte_teletravail: Optional[bool] = False  # ✅ Doit être là
    created_at: datetime
    updated_at: datetime
```

**Si non présent** → Redémarrer le backend après la correction.

### Problème 3 : Données pas enregistrées en base

**Tester l'API directement :**

```bash
curl -X PUT http://localhost:8080/api/users/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -d '{
    "salaire_minimum": 15000,
    "type_contrat_prefere": "CDI",
    "secteur_activite": "Informatique",
    "accepte_teletravail": true
  }'
```

**Vérifier en base :**
```sql
SELECT salaire_minimum, type_contrat_prefere, secteur_activite, accepte_teletravail
FROM users
WHERE email = 'votre_email@test.com';
```

### Problème 4 : Frontend ne recharge pas les données

**Ouvrir la console (F12) et regarder :**
```
User data: { ... }
```

**Si `salaire_minimum`, `type_contrat_prefere`, etc. sont `undefined` ou `null`** :
→ Le backend ne les envoie pas

**Solution :**
1. Redémarrer le backend
2. Se déconnecter et se reconnecter
3. Vérifier le token JWT

---

## 📊 Structure Attendue des Données

### Objet `user` dans le Frontend

```typescript
{
  id: 1,
  prenom: "hind",
  nom: "iraqi houssaini",
  email: "hind@gmail.com",
  telephone: "+212619787139",
  ville_preferee: "Fès",
  photo_profil: "/uploads/avatars/1_1234567890.jpg",
  salaire_minimum: 15000,          // ✅ Doit être présent
  type_contrat_prefere: "CDI",     // ✅ Doit être présent
  secteur_activite: "Informatique",// ✅ Doit être présent
  accepte_teletravail: true,       // ✅ Doit être présent
  created_at: "2025-11-20T...",
  updated_at: "2025-11-20T..."
}
```

### État `formData` dans le Composant

```typescript
{
  prenom: "hind",
  nom: "iraqi houssaini",
  email: "hind@gmail.com",
  telephone: "+212619787139",
  ville: "Fès",
  ville_preferee: "Fès",
  salaire_minimum: 15000,          // ✅ Chargé depuis user.salaire_minimum
  type_contrat_prefere: "CDI",     // ✅ Chargé depuis user.type_contrat_prefere
  accepte_remote: true,            // ✅ Chargé depuis user.accepte_teletravail
  secteur_activite: "Informatique" // ✅ Chargé depuis user.secteur_activite
}
```

---

## ✅ Checklist de Débogage

- [ ] Les colonnes existent en base (`\d users`)
- [ ] Les colonnes sont dans `UserResponse` (backend)
- [ ] Les colonnes sont dans `UserUpdate` (backend)
- [ ] L'API `/api/users/profile` (PUT) sauvegarde les champs
- [ ] L'API `/api/auth/me` (GET) retourne les champs
- [ ] Backend redémarré après les modifications
- [ ] Frontend redémarré après les modifications
- [ ] Se déconnecter et se reconnecter
- [ ] Console du navigateur affiche les données
- [ ] Requête SQL affiche les données en base

---

## 🎯 Comportement Final Attendu

### Scénario 1 : Première Visite

1. Ouvrir http://localhost:3000/dashboard/profil
2. ✅ **Formulaire rempli** avec les données existantes
3. ✅ **Préférences d'emploi remplies** (si déjà enregistrées)

### Scénario 2 : Modification

1. Modifier les préférences :
   ```
   Ville préférée : Casablanca
   Salaire minimum : 15000
   Type contrat : CDI
   Secteur : Informatique
   ☑ Télétravail
   ```
2. Cliquer "Enregistrer les modifications"
3. ✅ **Toast** : "Profil mis à jour avec succès !"
4. ✅ **Redirection automatique** vers `/dashboard` après 1 seconde

### Scénario 3 : Retour sur Profil

1. Cliquer sur "Mon Profil" dans le dropdown
2. ✅ **Toutes les données affichées** y compris les préférences
3. ✅ **Formulaire complètement rempli**

---

## 🚀 Actions à Faire Maintenant

### 1. Vérifier la Base de Données

```bash
psql -U postgres -d smarthire_db
```

```sql
-- Vérifier les colonnes
\d users

-- Ajouter si manquantes
ALTER TABLE users ADD COLUMN IF NOT EXISTS salaire_minimum INTEGER;
ALTER TABLE users ADD COLUMN IF NOT EXISTS type_contrat_prefere VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS secteur_activite VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS accepte_teletravail BOOLEAN DEFAULT FALSE;

-- Vérifier les données
SELECT * FROM users WHERE email = 'hind@gmail.com';

\q
```

### 2. Redémarrer Backend et Frontend

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

### 3. Tester

1. Aller sur http://localhost:3000/dashboard/profil
2. Ouvrir la console (F12)
3. Regarder le log : `User data: { ... }`
4. Modifier les préférences
5. Sauvegarder
6. Vérifier la redirection
7. Retourner sur profil
8. Vérifier que tout est affiché

---

**Faites ces tests et dites-moi ce qui s'affiche dans la console !** 🔍

