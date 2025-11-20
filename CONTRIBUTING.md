# 🤝 Guide de Contribution - SmartHire

Merci de votre intérêt pour contribuer à SmartHire ! Ce document vous guide à travers le processus de contribution.

## 📋 Table des Matières

- [Code de Conduite](#code-de-conduite)
- [Comment Contribuer](#comment-contribuer)
- [Configuration de l'Environnement de Développement](#configuration-de-lenvironnement-de-développement)
- [Standards de Code](#standards-de-code)
- [Processus de Pull Request](#processus-de-pull-request)
- [Signaler des Bugs](#signaler-des-bugs)
- [Proposer de Nouvelles Fonctionnalités](#proposer-de-nouvelles-fonctionnalités)

## 📜 Code de Conduite

En participant à ce projet, vous vous engagez à respecter les autres contributeurs et à maintenir un environnement respectueux et inclusif.

## 🚀 Comment Contribuer

Il existe plusieurs façons de contribuer à SmartHire :

1. **Signaler des bugs** 🐛
2. **Proposer de nouvelles fonctionnalités** 💡
3. **Améliorer la documentation** 📚
4. **Soumettre des corrections de code** 🔧
5. **Ajouter des tests** ✅

## 💻 Configuration de l'Environnement de Développement

### Prérequis

- Node.js 18+ et npm/pnpm
- Python 3.10+
- PostgreSQL 14+
- Git

### Étapes d'Installation

1. **Fork le repository** sur GitHub

2. **Clone votre fork**
```bash
git clone https://github.com/votre-username/SmartHire.git
cd SmartHire
```

3. **Ajouter le repository original comme remote**
```bash
git remote add upstream https://github.com/ranyaserraj/SmartHire.git
```

4. **Créer une branche pour votre contribution**
```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
# ou
git checkout -b fix/correction-bug
```

5. **Installer les dépendances Frontend**
```bash
npm install
# ou
pnpm install
```

6. **Installer les dépendances Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

7. **Configurer la base de données**
```bash
# Créer la base de données
createdb smarthire

# Copier et configurer .env
cp .env.example .env
# Éditer .env avec vos paramètres
```

## 📝 Standards de Code

### Frontend (TypeScript/React)

- **Style** : Suivre les conventions TypeScript et React
- **Formatage** : Utiliser Prettier (configuré dans le projet)
- **Linting** : Respecter les règles ESLint
- **Composants** : Préférer les composants fonctionnels avec hooks
- **Nommage** :
  - Composants : PascalCase (`MyComponent.tsx`)
  - Fichiers utilitaires : camelCase (`myUtils.ts`)
  - Constantes : UPPER_SNAKE_CASE

```typescript
// ✅ Bon exemple
export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);
  
  return <div>{user?.name}</div>;
}
```

### Backend (Python/FastAPI)

- **Style** : Suivre PEP 8
- **Type Hints** : Utiliser les annotations de type partout
- **Docstrings** : Documenter les fonctions et classes importantes
- **Nommage** :
  - Fonctions/variables : snake_case
  - Classes : PascalCase
  - Constantes : UPPER_SNAKE_CASE

```python
# ✅ Bon exemple
async def get_user_by_email(
    email: str,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Récupère un utilisateur par son email.
    
    Args:
        email: L'email de l'utilisateur
        db: Session de base de données
        
    Returns:
        Les informations de l'utilisateur
        
    Raises:
        HTTPException: Si l'utilisateur n'existe pas
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## 🔄 Processus de Pull Request

1. **Assurez-vous que votre branche est à jour**
```bash
git fetch upstream
git rebase upstream/main
```

2. **Testez vos modifications**
```bash
# Frontend
npm run build
npm run lint

# Backend
pytest
```

3. **Committez vos changements**
```bash
git add .
git commit -m "feat: description de la fonctionnalité"
```

**Format des messages de commit** :
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage, style
- `refactor:` Refactorisation
- `test:` Ajout de tests
- `chore:` Maintenance

4. **Poussez votre branche**
```bash
git push origin feature/ma-nouvelle-fonctionnalite
```

5. **Créez une Pull Request** sur GitHub

### Checklist pour la Pull Request

- [ ] Le code compile sans erreur
- [ ] Les tests passent
- [ ] La documentation est à jour
- [ ] Les messages de commit sont clairs
- [ ] Le code respecte les standards du projet
- [ ] Les nouvelles fonctionnalités sont testées

## 🐛 Signaler des Bugs

Lorsque vous signalez un bug, incluez :

1. **Titre clair et descriptif**
2. **Étapes pour reproduire le bug**
3. **Comportement attendu vs comportement observé**
4. **Captures d'écran** (si applicable)
5. **Environnement** :
   - OS et version
   - Version de Node.js/Python
   - Version du navigateur (si frontend)

### Template de Bug Report

```markdown
**Description**
Description claire et concise du bug.

**Étapes pour reproduire**
1. Aller à '...'
2. Cliquer sur '...'
3. Voir l'erreur

**Comportement attendu**
Ce qui devrait se passer.

**Captures d'écran**
Si applicable, ajouter des captures d'écran.

**Environnement**
- OS: [ex. Windows 11]
- Node.js: [ex. 18.17.0]
- Navigateur: [ex. Chrome 120]
```

## 💡 Proposer de Nouvelles Fonctionnalités

Avant de proposer une nouvelle fonctionnalité :

1. **Vérifiez** qu'elle n'existe pas déjà ou n'est pas en développement
2. **Ouvrez une issue** pour discuter de la fonctionnalité
3. **Décrivez** :
   - Le problème que cela résout
   - La solution proposée
   - Les alternatives considérées
   - L'impact sur le système existant

### Template de Feature Request

```markdown
**Problème à résoudre**
Description claire du problème.

**Solution proposée**
Comment vous voyez la fonctionnalité.

**Alternatives**
Autres approches considérées.

**Contexte additionnel**
Captures d'écran, mockups, etc.
```

## 📚 Documentation

Si vous modifiez le code, pensez à :

1. Mettre à jour le `README.md` si nécessaire
2. Ajouter des commentaires pour les parties complexes
3. Mettre à jour les docstrings/JSDoc
4. Créer/modifier des fichiers de documentation dans `/docs` si applicable

## 🙏 Remerciements

Merci d'avoir pris le temps de contribuer à SmartHire ! Votre aide est précieuse pour améliorer l'application.

---

**Questions ?** N'hésitez pas à ouvrir une issue ou à contacter les mainteneurs.

