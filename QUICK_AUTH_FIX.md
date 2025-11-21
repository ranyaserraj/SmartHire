# 🚀 Fix Rapide - Authentification

## 📋 Diagnostic en 3 Étapes

### 1️⃣ Tester le Backend (30 secondes)

```bash
cd backend
python test_auth.py
```

**Si tous les tests passent ✅** → Le backend fonctionne, problème côté frontend  
**Si ça échoue ❌** → Suivre les étapes ci-dessous

---

## ✅ Si le Backend Fonctionne

### Le problème est côté Frontend

1. **Vérifier que le frontend tourne :**
   ```bash
   npm run dev
   ```

2. **Ouvrir la console du navigateur (F12)**
   - Aller sur `http://localhost:3000/auth`
   - Regarder les erreurs dans la console

3. **Vérifier l'URL dans `contexts/AuthContext.tsx` ligne 64, 99, 163, 194 :**
   ```typescript
   "http://localhost:8080/api/auth/..."
   ```

4. **Vérifier que `USE_MOCK_AUTH = false` dans `contexts/AuthContext.tsx` ligne 6**

---

## ❌ Si le Backend Échoue

### Étape A : Redémarrer le Serveur

```bash
# Dans le terminal backend, appuyez sur Ctrl+C
# Puis relancer :
cd C:\Users\pc\Downloads\code\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

**Attendez de voir :**
```
🚀 SmartHire API Started
📚 Documentation: http://localhost:8080/docs
```

### Étape B : Si erreur "ModuleNotFoundError: No module named 'pdfplumber'"

```bash
pip install pdfplumber rapidfuzz python-dateutil
```

Puis redémarrer le serveur (Ctrl+C + relancer).

### Étape C : Retester

```bash
cd backend
python test_auth.py
```

---

## 🎯 Test Manuel Rapide

### Dans le Navigateur

1. **Ouvrir** `http://localhost:3000/auth`
2. **Onglet "S'inscrire"**
3. **Remplir :**
   - Prénom : Test
   - Nom : User  
   - Email : test@example.com
   - Mot de passe : test123456
   - Confirmer : test123456
4. **Cliquer "Créer mon compte"**

**✅ Résultat attendu :** "Inscription réussie !" + redirection vers `/dashboard`

---

## 🆘 Si Rien ne Marche

### Vérifications Finales

```bash
# 1. PostgreSQL tourne ?
psql -U postgres -d smarthire_db
# Mot de passe : ranyaa
# Si ça se connecte, c'est bon ✅

# 2. Backend sur port 8080 ?
curl http://localhost:8080/docs
# Si ça répond, c'est bon ✅

# 3. Frontend sur port 3000 ?
curl http://localhost:3000
# Si ça répond, c'est bon ✅
```

---

## 📸 Capture des Erreurs

Si ça ne fonctionne toujours pas :

### Backend
- Copier l'erreur du terminal où tourne le serveur

### Frontend
- F12 → Console
- Copier les erreurs en rouge

### Test
```bash
cd backend
python test_auth.py > test_result.txt
# Partager test_result.txt
```

---

## 🎬 Démarrage Complet (Fresh Start)

```bash
# Terminal 1 : Backend
cd C:\Users\pc\Downloads\code\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Terminal 2 : Frontend
cd C:\Users\pc\Downloads\code
npm run dev

# Terminal 3 : Test
cd C:\Users\pc\Downloads\code\backend
python test_auth.py
```

**Tout devrait être vert ✅**

---

**Pour plus de détails :** Voir `FIX_AUTH.md`

