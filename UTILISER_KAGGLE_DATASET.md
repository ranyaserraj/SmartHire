# 🎯 Utiliser le Dataset Kaggle pour les Compétences

## 📋 Avantage du Dataset Kaggle

Le dataset **UpdatedResumeDataSet.csv** de Kaggle contient :
- ✅ **~1000 CV réels**
- ✅ Compétences réellement utilisées par des candidats
- ✅ Vocabulaire professionnel actuel
- ✅ **Gratuit** et prêt à l'emploi
- ✅ Bien plus pertinent que l'échantillon de 139 compétences

**Résultat attendu :** 500-1000 compétences extraites de vrais CV

---

## 📥 Étape 1 : Télécharger le Dataset

### Option A : Depuis Kaggle (Recommandé)

1. **Aller sur Kaggle :**
   ```
   https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
   ```

2. **Télécharger le fichier :**
   - Cliquer sur "Download" (nécessite un compte Kaggle gratuit)
   - Télécharger `UpdatedResumeDataSet.csv`

3. **Placer le fichier :**
   ```
   C:\Users\pc\Downloads\code\backend\data\UpdatedResumeDataSet.csv
   ```

### Option B : Dataset Alternatif

Si celui-ci n'est pas disponible, cherchez sur Kaggle :
- "resume dataset"
- "cv dataset"
- "job skills dataset"

Le script accepte n'importe quel CSV contenant des colonnes avec du texte de CV.

---

## ⚙️ Étape 2 : Parser le Dataset

### Exécuter le script :

```bash
cd backend
python parse_kaggle_resumes.py
```

### Ce que le script fait :

1. ✅ Lit le CSV avec gestion automatique de l'encodage
2. ✅ Extrait toutes les compétences de tous les CV
3. ✅ Classifie en technical vs soft skills
4. ✅ Compte la fréquence de chaque compétence
5. ✅ Crée un fichier JSON propre

### Résultat attendu :

```
📊 Parsing du Dataset Kaggle - UpdatedResumeDataSet.csv
==================================================================

📂 Lecture du fichier: UpdatedResumeDataSet.csv
   ✅ Succès avec utf-8

📊 Dataset chargé:
   Lignes: 962
   Colonnes: ['Category', 'Resume']

🔍 Extraction des compétences...
   Traité: 100/962 CV...
   Traité: 200/962 CV...
   ...
   Traité: 962/962 CV...

✅ Extraction terminée!
   Total CV analysés: 962
   Compétences uniques: 847
   Catégories: 25

🔝 Top 20 compétences les plus fréquentes:
   1. Python                        - 524 fois
   2. Java                          - 487 fois
   3. SQL                           - 423 fois
   4. Machine Learning              - 398 fois
   5. JavaScript                    - 365 fois
   ...

💾 Fichier créé: backend/data/kaggle_skills.json
   Taille: 45.2 KB
   - Compétences techniques: 789
   - Soft skills: 58
```

---

## 📊 Étape 3 : Vérifier le Résultat

### Le fichier créé : `backend/data/kaggle_skills.json`

**Structure :**
```json
{
  "technical_skills": [
    "Python",
    "JavaScript",
    "Java",
    "SQL",
    "React",
    "Node.js",
    ...
  ],
  "soft_skills": [
    "Leadership",
    "Communication",
    "Teamwork",
    ...
  ],
  "metadata": {
    "total_skills": 847,
    "technical": 789,
    "soft": 58,
    "source": "Kaggle UpdatedResumeDataSet",
    "total_cvs_analyzed": 962
  },
  "top_skills": [
    {"skill": "Python", "frequency": 524},
    {"skill": "Java", "frequency": 487},
    ...
  ]
}
```

---

## 🚀 Étape 4 : Activer la V3 avec Kaggle

### La V3 chargera automatiquement le dataset Kaggle en priorité !

**Ordre de priorité dans `esco_loader.py` :**
1. ✅ **kaggle_skills.json** (si existe) ← Votre dataset
2. esco_skills_complete.json
3. esco_skills_extended.json
4. esco_skills_full.csv
5. esco_skills_sample.json (échantillon)

### Activer la V3 :

**Modifier `backend/app/api/cvs.py` :**

```python
# Ligne 12
from ..services.cv_extractor_v3 import CVExtractorV3

# Ligne 61
extractor = CVExtractorV3()
```

### Redémarrer le serveur :

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Vous verrez :

```
🚀 Initialisation CV Extractor V3...
🎯 Chargement du dataset Kaggle (CV réels)...
✅ 847 compétences chargées (échantillon)
   - Techniques: 789
   - Soft skills: 58
✅ CV Extractor V3 prêt
   📊 ESCO: 847 compétences chargées
```

---

## 📊 Comparaison

| Dataset | Compétences | Source | Qualité |
|---------|-------------|--------|---------|
| **Échantillon** | 139 | Manuel | ⭐⭐⭐ |
| **Kaggle** | 500-1000 | CV réels | ⭐⭐⭐⭐⭐ |
| **ESCO** | 13 000+ | UE officiel | ⭐⭐⭐⭐ |

### Recommandation :

**Utilisez Kaggle** pour commencer (5 minutes) :
- ✅ CV réels, vocabulaire actuel
- ✅ Rapide à installer
- ✅ Très pertinent

**Plus tard, combinez avec ESCO** pour exhaustivité maximale

---

## 🔄 Option Avancée : Fusionner Kaggle + ESCO

Si vous avez les deux datasets :

```bash
cd backend
python download_esco_complete.py
# Choisir option 3: Fusionner les datasets
```

**Résultat :** Dataset combiné avec 13 000+ compétences ESCO + celles de Kaggle

---

## 🎯 Résumé : Actions Immédiates

1. ✅ Télécharger `UpdatedResumeDataSet.csv` depuis Kaggle
2. ✅ Placer dans `backend/data/`
3. ✅ Exécuter `python parse_kaggle_resumes.py`
4. ✅ Activer V3 dans `cvs.py`
5. ✅ Redémarrer le serveur
6. ✅ Tester avec des CV réels

**Temps total : 5-10 minutes**  
**Résultat : 500-1000 compétences de CV réels** 🎉

---

## 🆘 Dépannage

### Erreur : "Fichier introuvable"

**Solution :** Vérifiez le chemin exact :
```
backend/data/UpdatedResumeDataSet.csv
```

### Erreur : "No module named 'pandas'"

**Solution :**
```bash
pip install pandas
```

### Peu de compétences extraites

**Cause :** Le dataset Kaggle que vous avez est différent

**Solution :** Ouvrez le CSV et vérifiez les noms de colonnes. Modifiez le script si nécessaire.

---

**Prêt à extraire 847+ compétences de CV réels !** 🚀

