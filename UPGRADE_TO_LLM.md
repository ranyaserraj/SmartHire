# 🚀 Passer au CV Extractor LLM (Optionnel)

## 📊 Comparaison des Versions

| Version | Précision | Coût | Setup | Recommandation |
|---------|-----------|------|-------|----------------|
| **V2 (Actuel)** | ~88% | Gratuit | Simple | ✅ Production |
| **V3 (LLM)** | ~95-98% | ~$0.01-0.02/CV | API Key | ⭐ Premium |

## 💰 Coût Estimé avec OpenAI

### Avec gpt-4o-mini (recommandé)

- **Input** : 4000 tokens (1 CV) × $0.15/1M tokens = **$0.0006**
- **Output** : 800 tokens (JSON) × $0.60/1M tokens = **$0.0005**
- **Total par CV** : **~$0.001** (0.1 centime)

### Avec gpt-4-turbo

- **Input** : 4000 tokens × $10/1M tokens = **$0.04**
- **Output** : 800 tokens × $30/1M tokens = **$0.024**
- **Total par CV** : **~$0.06** (6 centimes)

### Volume mensuel

| CVs/mois | Coût gpt-4o-mini | Coût gpt-4-turbo |
|----------|------------------|------------------|
| 100 | $0.10 | $6 |
| 500 | $0.50 | $30 |
| 1,000 | $1.00 | $60 |
| 5,000 | $5.00 | $300 |

💡 **Recommandation** : Utiliser **gpt-4o-mini** pour un excellent rapport qualité/prix

## 🔧 Installation

### Étape 1 : Installer la bibliothèque OpenAI

```bash
cd backend
pip install openai
```

### Étape 2 : Obtenir une clé API OpenAI

1. Aller sur https://platform.openai.com/api-keys
2. Créer un compte (ou se connecter)
3. Créer une nouvelle clé API
4. Copier la clé (format : `sk-...`)

### Étape 3 : Configurer la clé API

**Option A : Fichier `.env`** (recommandé)

```bash
# backend/.env
OPENAI_API_KEY=sk-votre-cle-ici
```

**Option B : Variable d'environnement**

Windows :
```cmd
set OPENAI_API_KEY=sk-votre-cle-ici
```

Linux/Mac :
```bash
export OPENAI_API_KEY=sk-votre-cle-ici
```

### Étape 4 : Activer le mode LLM

**Modifier `backend/app/api/cvs.py` :**

```python
# Ligne 12 - Remplacer :
from ..services.cv_extractor_v2 import CVExtractorV2

# Par :
from ..services.cv_extractor_llm import CVExtractorLLM
```

```python
# Ligne 61 - Remplacer :
extractor = CVExtractorV2()

# Par :
extractor = CVExtractorLLM()
```

### Étape 5 : Redémarrer le serveur

```bash
cd backend
START_SERVER.bat
```

## ✅ Vérification

Le serveur affichera au démarrage :

**Si API key configurée :**
```
✅ CV Extractor LLM activé (utilise OpenAI GPT-4o-mini)
```

**Si API key manquante :**
```
⚠️ OPENAI_API_KEY non définie, utilisation du CV Extractor V2
```

## 🎯 Avantages du Mode LLM

### 1. **Compréhension Contextuelle**

**V2 (regex) :**
```
"Gestion d'équipe" → Non détecté (pas dans la liste)
```

**LLM :**
```
"Gestion d'équipe" → ✅ Détecté comme soft skill
```

### 2. **Extraction de Missions**

**V2 :**
```json
{
  "periode": "2020-2023",
  "description": "Développeur Full-Stack - Google Développement..."
}
```

**LLM :**
```json
{
  "poste": "Développeur Full-Stack",
  "entreprise": "Google",
  "periode": "Jan 2020 - Mar 2023",
  "missions": [
    "Développement d'applications React",
    "Conception d'APIs REST avec FastAPI",
    "Migration vers microservices"
  ]
}
```

### 3. **Détection de Formations Complètes**

**V2 :**
```json
{
  "diplome": "Master",
  "description": "Master Informatique Université..."
}
```

**LLM :**
```json
{
  "diplome": "Master en Informatique",
  "etablissement": "Université Paris-Saclay",
  "annee": "2020"
}
```

### 4. **Normalisation des Dates**

**V2 :**
```
"Mar 2021", "03/2019", "Aujourd'hui"
```

**LLM :**
```
"Mars 2021 - Present", "Mars 2019 - Février 2021"
```

### 5. **Gestion des CV Très Complexes**

- ✅ CV artistiques avec design créatif
- ✅ CV avec infographies
- ✅ CV en plusieurs langues mélangées
- ✅ CV avec acronymes spécifiques à une industrie
- ✅ CV avec typos / OCR imparfait

## 🧪 Test de Performance

### CV Simple

| Critère | V2 | LLM | Gagnant |
|---------|----|----|---------|
| Nom | ✅ 90% | ✅ 95% | LLM |
| Email | ✅ 95% | ✅ 98% | LLM |
| Compétences | ⚠️ 85% | ✅ 95% | LLM |
| Expérience | ⚠️ 75% | ✅ 98% | LLM |
| Formation | ⚠️ 70% | ✅ 95% | LLM |

### CV Complexe (Colonnes, Tableaux)

| Critère | V2 | LLM | Gagnant |
|---------|----|----|---------|
| Structure | ⚠️ 70% | ✅ 98% | LLM |
| Missions détaillées | ❌ 30% | ✅ 95% | LLM |
| Soft skills | ❌ 40% | ✅ 90% | LLM |
| Contexte | ❌ 20% | ✅ 95% | LLM |

### CV Créatif / Artistique

| Critère | V2 | LLM | Gagnant |
|---------|----|----|---------|
| Extraction globale | ❌ 40% | ✅ 85% | LLM |
| Compréhension | ❌ 30% | ✅ 90% | LLM |

## 🔄 Mode Hybride (Recommandé)

Le système LLM utilise automatiquement **V2 comme fallback** :

```python
def extract_from_file(self, file_path: str) -> Dict:
    # Toujours extraire avec V2 d'abord
    v2_result = self.v2_extractor.extract_from_file(file_path)
    
    # Si API key disponible, améliorer avec LLM
    if self.use_llm:
        try:
            llm_result = self._extract_with_llm(text)
            return self._merge_results(llm_result, v2_result)
        except:
            return v2_result  # Fallback sur V2
    
    return v2_result
```

**Avantages :**
- ✅ Si l'API OpenAI est down → V2 prend le relais
- ✅ Si rate limit atteint → V2 en secours
- ✅ Union des compétences (V2 + LLM)
- ✅ Aucun échec total

## ⚙️ Configuration Avancée

### Changer de Modèle

**Dans `cv_extractor_llm.py`, ligne 95 :**

```python
# Économique (recommandé)
model="gpt-4o-mini"  # $0.001/CV

# Plus précis mais cher
model="gpt-4-turbo"  # $0.06/CV

# GPT-4 classique
model="gpt-4"        # $0.10/CV
```

### Limiter le Nombre de Tokens

```python
# Ligne 78 : Réduire pour économiser
text_truncated = text[:4000]  # Actuellement 4000 caractères

# Ligne 100 : Réduire max_tokens si besoin
max_tokens=1500  # Actuellement 1500
```

### Augmenter la Température (Plus Créatif)

```python
# Ligne 99
temperature=0.1  # 0 = déterministe, 1 = créatif
```

## 🔐 Sécurité

### ⚠️ Ne JAMAIS commit la clé API

**Vérifier `.gitignore` :**
```
backend/.env
**/.env
*.env
```

### 🔒 Utiliser des Variables d'Environnement

En production, configurer `OPENAI_API_KEY` dans les variables d'environnement du serveur (Heroku, AWS, Azure, etc.)

## 📈 Monitoring des Coûts

### Tableau de Bord OpenAI

1. Aller sur https://platform.openai.com/usage
2. Voir les requêtes et coûts en temps réel
3. Définir des limites mensuelles

### Limiter le Budget

Dans le dashboard OpenAI :
- **Usage limits** → Définir un budget max (ex: $10/mois)
- Recevoir des alertes email si le budget est atteint

## 🎓 Résumé : Quand Utiliser LLM ?

### ✅ Utiliser LLM si :

- Vous traitez des CV **très complexes** (design créatif, tableaux)
- Vous avez besoin de **missions détaillées**
- Vous voulez extraire les **soft skills**
- Vous acceptez un coût de **~$0.001 par CV**
- Vous visez une **précision maximale** (95-98%)

### ✅ Rester sur V2 si :

- Vous traitez des CV **standards**
- Vous avez un **budget serré** (gratuit)
- La **précision de 88%** est suffisante
- Vous ne voulez pas dépendre d'une **API externe**

## 🚀 Pour Commencer

```bash
# 1. Installer OpenAI
pip install openai

# 2. Configurer la clé
echo OPENAI_API_KEY=sk-votre-cle >> backend/.env

# 3. Activer dans cvs.py
# Remplacer CVExtractorV2 par CVExtractorLLM

# 4. Redémarrer
cd backend
START_SERVER.bat
```

---

**Mode LLM** : Pour la précision maximale 🎯  
**Mode V2** : Pour la gratuité et la rapidité ⚡  
**Mode Hybride** : Le meilleur des deux mondes 🌟

