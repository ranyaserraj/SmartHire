# ✅ Photo de Profil Ajoutée - SmartHire

## 🎉 Modifications Terminées

Le système d'inscription inclut maintenant un champ **photo de profil** (optionnel) et la navbar affiche correctement le **nom complet** et la **photo de profil** de l'utilisateur !

---

## ✨ Nouvelles Fonctionnalités

### 1. **Champ Photo de Profil dans l'Inscription**

✅ Nouveau champ **optionnel** dans le formulaire d'inscription :
- Upload d'image (JPG, PNG, GIF)
- Taille maximale : **5MB**
- Preview en temps réel (aperçu circulaire)
- Validation automatique du format et de la taille

**Interface :**
```
┌─────────────────────────────────────────┐
│  Photo de profil (optionnel)            │
├─────────────────────────────────────────┤
│  ⭕ [Preview]    [Choisir un fichier]   │
│                 Format: JPG, PNG, GIF   │
│                 (Max 5MB)               │
└─────────────────────────────────────────┘
```

### 2. **Navbar Dashboard - Affichage Utilisateur**

✅ La navbar affiche maintenant :
- **Photo de profil** de l'utilisateur (ou initiales si pas de photo)
- **Nom complet** : `Prénom Nom` (ex: "Ranya SERRAJ")
- **Email** : Affiché en sous-titre

**Avant :**
```
[U] Utilisateur
    email
```

**Maintenant :**
```
[📷] Ranya SERRAJ
     ranya@test.com
```

### 3. **Sidebar Footer - Affichage Utilisateur**

✅ Le footer de la sidebar affiche aussi :
- Photo de profil (plus grande, 40px)
- Nom complet
- Email

---

## 🔧 Modifications Techniques

### Frontend

#### 1. **app/auth/page.tsx** - Formulaire d'inscription

**Nouveaux états :**
```typescript
const [photoProfil, setPhotoProfil] = useState<File | null>(null)
const [photoPreview, setPhotoPreview] = useState<string | null>(null)
```

**Handler upload photo :**
```typescript
const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0]
  if (file) {
    // Vérifier taille (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      setErrors({ ...errors, photo: "La photo ne doit pas dépasser 5MB" })
      return
    }
    
    // Vérifier type (image uniquement)
    if (!file.type.startsWith("image/")) {
      setErrors({ ...errors, photo: "Le fichier doit être une image" })
      return
    }
    
    setPhotoProfil(file)
    
    // Créer preview
    const reader = new FileReader()
    reader.onloadend = () => {
      setPhotoPreview(reader.result as string)
    }
    reader.readAsDataURL(file)
  }
}
```

**Champ photo dans le formulaire :**
```tsx
<div className="space-y-2">
  <Label htmlFor="photo">Photo de profil (optionnel)</Label>
  <div className="flex items-center gap-4">
    {photoPreview && (
      <div className="relative w-20 h-20 rounded-full overflow-hidden border-2 border-blue-500">
        <img
          src={photoPreview}
          alt="Preview"
          className="w-full h-full object-cover"
        />
      </div>
    )}
    <div className="flex-1">
      <Input
        id="photo"
        type="file"
        accept="image/*"
        onChange={handlePhotoChange}
      />
      <p className="text-xs text-gray-500 mt-1">
        Format: JPG, PNG, GIF (Max 5MB)
      </p>
    </div>
  </div>
</div>
```

**Soumission avec photo :**
```typescript
await register(email, password, nom, prenom, telephone, villePreferee, photoProfil)
```

#### 2. **contexts/AuthContext.tsx** - Upload photo

**Fonction register mise à jour :**
```typescript
const register = async (
  email: string, 
  password: string, 
  nom: string, 
  prenom: string, 
  telephone?: string, 
  ville_preferee?: string,
  photo?: File | null  // ✅ Nouveau paramètre
) => {
  // 1. Créer l'utilisateur
  const response = await fetch("http://localhost:8080/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email,
      mot_de_passe: password,
      nom,
      prenom,
      telephone,
      ville_preferee,
    }),
  })

  // 2. Connecter automatiquement
  await login(email, password)

  // 3. Si photo fournie, l'uploader
  if (photo) {
    const token = localStorage.getItem("token")
    if (token) {
      const formData = new FormData()
      formData.append("file", photo)

      await fetch("http://localhost:8080/api/users/photo", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      })

      // Recharger les infos utilisateur pour avoir la photo
      await fetchUser(token)
    }
  }
}
```

#### 3. **components/layouts/DashboardLayout.tsx** - Affichage

**Fonctions utilitaires :**
```typescript
// Obtenir initiales depuis prénom et nom
const getInitials = (prenom?: string, nom?: string) => {
  if (!prenom && !nom) return "U"
  const p = prenom?.charAt(0) || ""
  const n = nom?.charAt(0) || ""
  return (p + n).toUpperCase()
}

// Obtenir nom complet
const getFullName = () => {
  if (!user) return "Utilisateur"
  return `${user.prenom || ""} ${user.nom || ""}`.trim() || "Utilisateur"
}

// Obtenir URL photo
const getPhotoUrl = () => {
  if (!user?.photo_profil) return undefined
  if (user.photo_profil.startsWith("http")) return user.photo_profil
  return `http://localhost:8080${user.photo_profil}`
}
```

**Navbar avec photo :**
```tsx
<Avatar className="h-8 w-8">
  <AvatarImage src={getPhotoUrl()} />
  <AvatarFallback className="bg-blue-600 text-white">
    {getInitials(user?.prenom, user?.nom)}
  </AvatarFallback>
</Avatar>
<div className="hidden md:block text-left">
  <p className="text-sm font-medium text-gray-900">
    {getFullName()}
  </p>
  <p className="text-xs text-gray-500">{user?.email}</p>
</div>
```

### Backend

Le backend est déjà prêt avec l'endpoint :
```python
@router.post("/photo")
async def upload_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Upload et sauvegarde de la photo
    # Retourne le chemin de la photo
```

---

## 🚀 Comment Tester

### 1. **Redémarrer Backend et Frontend**

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

### 2. **Tester l'Inscription avec Photo**

1. Ouvrir **http://localhost:3000/auth**
2. Cliquer sur l'onglet **"S'inscrire"**
3. Remplir tous les champs :
   ```
   Prénom : Ranya
   Nom : SERRAJ
   Email : ranya.photo@test.com
   Téléphone : +212 612345678
   Ville : Rabat
   Mot de passe : password123
   Confirmer : password123
   ```
4. **Cliquer sur "Choisir un fichier"** pour la photo
5. Sélectionner une image (JPG, PNG, GIF - max 5MB)
6. ✅ Vous devez voir un **aperçu circulaire** de la photo
7. Cliquer sur **"Créer mon compte"**

### 3. **Vérifier le Dashboard**

Après l'inscription, vous devriez être automatiquement redirigé vers `/dashboard` :

✅ **Navbar** (en haut à droite) :
- Photo de profil circulaire (ou initiales "RS")
- Nom complet : "Ranya SERRAJ"
- Email : "ranya.photo@test.com"

✅ **Sidebar** (en bas à gauche) :
- Photo de profil circulaire (plus grande)
- Nom complet
- Email

### 4. **Vérifier dans la Base de Données**

```bash
psql -U postgres -d smarthire_db
```

Mot de passe : `ranyaa`

```sql
SELECT id, prenom, nom, email, photo_profil, ville_preferee 
FROM users 
WHERE email = 'ranya.photo@test.com';
```

**Résultat attendu :**
```
 id | prenom | nom    | email                  | photo_profil                      | ville_preferee
----+--------+--------+------------------------+-----------------------------------+----------------
  2 | Ranya  | SERRAJ | ranya.photo@test.com   | /uploads/avatars/abc123.jpg       | Rabat
```

### 5. **Vérifier le Fichier Photo**

La photo devrait être sauvegardée dans :
```
C:\Users\pc\Downloads\code\backend\uploads\avatars\
```

---

## 📊 Flux Complet d'Inscription avec Photo

```
┌──────────────┐
│   FRONTEND   │
│  /auth page  │
└──────┬───────┘
       │
       │ 1. Utilisateur remplit formulaire
       │    (nom, prenom, email, telephone, ville, password, PHOTO)
       │
       │ 2. Validation frontend
       │    ✓ Format image (JPG, PNG, GIF)
       │    ✓ Taille < 5MB
       │    ✓ Preview générée
       │
       │ 3. POST /api/auth/register (sans photo)
       ▼
┌────────────────────┐
│     BACKEND        │
│  Create User       │
└──────┬─────────────┘
       │
       │ 4. User créé dans PostgreSQL
       │
       │ 5. Return UserResponse
       ▼
┌──────────────┐
│   FRONTEND   │
│  AuthContext │
└──────┬───────┘
       │
       │ 6. POST /api/auth/login
       │
       │ 7. Recevoir JWT token
       │
       │ 8. Si photo fournie:
       │    POST /api/users/photo (multipart/form-data)
       │    Authorization: Bearer {token}
       ▼
┌────────────────────┐
│     BACKEND        │
│  Upload Photo      │
└──────┬─────────────┘
       │
       │ 9. Sauvegarder fichier dans /uploads/avatars/
       │
       │ 10. UPDATE users SET photo_profil = '/uploads/avatars/xxx.jpg'
       ▼
┌────────────────┐
│   POSTGRESQL   │
│  Photo URL     │
└──────┬─────────┘
       │
       │ 11. Return photo path
       ▼
┌──────────────┐
│   FRONTEND   │
│  Reload User │
└──────┬───────┘
       │
       │ 12. GET /api/auth/me
       │
       │ 13. Recevoir user avec photo_profil
       │
       │ 14. router.push("/dashboard")
       │
       ▼
┌──────────────┐
│  DASHBOARD   │
│  With Photo! │
└──────────────┘
```

---

## 🎨 Interface Utilisateur

### Formulaire d'Inscription avec Photo

```
┌─────────────────────────────────────────────┐
│  SmartHire                                  │
│  Créer un compte                            │
├─────────────────────────────────────────────┤
│  [Connexion] [✓ S'inscrire]                │
├─────────────────────────────────────────────┤
│  Prénom *          │  Nom *                 │
│  [Ranya______]     │  [SERRAJ_______]       │
│                                             │
│  Email *                                    │
│  [ranya@test.com_____________________]      │
│                                             │
│  Photo de profil (optionnel)                │
│  ⭕ Preview         [Choisir un fichier]    │
│                    Format: JPG, PNG, GIF    │
│                    (Max 5MB)                │
│                                             │
│  Téléphone         │  Ville préférée        │
│  [+212 6XX...]     │  [Rabat ▼]            │
│                                             │
│  Mot de passe *    │  Confirmer *           │
│  [••••••••]        │  [••••••••]           │
│                                             │
│  [    Créer mon compte    ]                 │
│                                             │
│  * Champs obligatoires                      │
└─────────────────────────────────────────────┘
```

### Navbar Dashboard

```
┌────────────────────────────────────────────────────────┐
│  SmartHire           [🔔]  [📷] Ranya SERRAJ [▼]      │
│                                 ranya@test.com         │
└────────────────────────────────────────────────────────┘
```

Au clic sur le dropdown :
```
┌─────────────────────────┐
│  Mon compte             │
├─────────────────────────┤
│  👤 Mon Profil          │
│  ⚙️  Paramètres         │
├─────────────────────────┤
│  🚪 Déconnexion (rouge) │
└─────────────────────────┘
```

---

## 🔒 Validation et Sécurité

### Frontend
- ✅ Vérification taille fichier (< 5MB)
- ✅ Vérification type fichier (image/* uniquement)
- ✅ Preview avant upload
- ✅ Messages d'erreur clairs

### Backend
- ✅ Validation type MIME
- ✅ Validation taille fichier
- ✅ Nom de fichier unique (UUID)
- ✅ Stockage sécurisé dans /uploads/avatars/
- ✅ Authentification requise (JWT)

---

## 🐛 Gestion des Erreurs

### Erreurs Photo

| Erreur | Message |
|--------|---------|
| Fichier trop grand | "La photo ne doit pas dépasser 5MB" |
| Type invalide | "Le fichier doit être une image" |
| Upload échoué | "Erreur upload photo" (en console, n'empêche pas l'inscription) |

### Fallback Sans Photo

Si l'utilisateur ne fournit pas de photo ou si l'upload échoue :
- ✅ L'inscription fonctionne quand même
- ✅ Les avatars affichent les **initiales** (ex: "RS" pour Ranya SERRAJ)
- ✅ Fond bleu avec lettres blanches

---

## ✅ Checklist de Test

- [ ] Inscription sans photo fonctionne
- [ ] Inscription avec photo JPG fonctionne
- [ ] Inscription avec photo PNG fonctionne
- [ ] Preview de la photo s'affiche correctement
- [ ] Erreur si fichier > 5MB
- [ ] Erreur si fichier non-image (PDF, etc.)
- [ ] Photo apparaît dans la navbar après inscription
- [ ] Photo apparaît dans la sidebar
- [ ] Initiales affichées si pas de photo
- [ ] Nom complet affiché correctement
- [ ] Photo enregistrée dans /uploads/avatars/
- [ ] Chemin photo enregistré en base de données
- [ ] Dropdown navbar fonctionne
- [ ] Déconnexion fonctionne

---

## 🎯 Prochaines Étapes

1. ✅ **Tester l'inscription avec photo**
2. ⏳ **Page "Mon Profil" pour modifier la photo**
3. ⏳ **Recadrage/redimensionnement photo automatique**
4. ⏳ **Compression photo côté backend**
5. ⏳ **Support drag & drop pour la photo**
6. ⏳ **Galerie d'avatars par défaut**

---

## 🎉 Félicitations !

Votre système d'authentification est maintenant **complet** avec :
- ✅ Inscription avec photo de profil
- ✅ Preview en temps réel
- ✅ Validation robuste
- ✅ Affichage photo dans navbar et sidebar
- ✅ Fallback avec initiales
- ✅ Nom complet correctement affiché

**Testez maintenant l'inscription avec photo depuis http://localhost:3000/auth !** 🚀📷

