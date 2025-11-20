# 📄 Fonctionnalité d'Extraction Automatique des Données du CV

## ✨ Description

Cette fonctionnalité permet d'extraire automatiquement les informations d'un CV (PDF ou image) lors de son téléchargement. L'utilisateur peut ensuite vérifier et corriger les données extraites avant de les enregistrer.

## 🎯 Fonctionnalités

- **Extraction automatique** des informations du CV :
  - Nom complet
  - Email
  - Téléphone
  - Ville
  - Compétences techniques
  - Expérience professionnelle
  - Formation
  - Langues

- **Formulaire de vérification** :
  - Pré-rempli avec les données extraites
  - Édition facile de chaque champ
  - Ajout/suppression de compétences
  - Interface intuitive et moderne

- **Support multi-formats** :
  - PDF (extraction de texte native)
  - Images (OCR avec Tesseract)

## 📦 Installation

### 1. Dépendances Python

Installez les nouvelles dépendances Python :

```bash
cd backend
pip install PyPDF2==3.0.1 pytesseract==0.3.10
```

**Note pour Windows :** Tesseract OCR doit être installé séparément :
1. Téléchargez Tesseract depuis : https://github.com/UB-Mannheim/tesseract/wiki
2. Installez-le (par défaut dans `C:\Program Files\Tesseract-OCR`)
3. Ajoutez-le au PATH système ou configurez le chemin dans le code

**Note pour Linux :**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-fra tesseract-ocr-eng
```

**Note pour macOS :**
```bash
brew install tesseract tesseract-lang
```

### 2. Migration de Base de Données

Ajoutez le champ `ville` à la table `cvs` :

```bash
cd backend
psql -U postgres -d smarthire -f app/migrations/add_ville_to_cvs.sql
```

Ou exécutez manuellement dans PostgreSQL :
```sql
ALTER TABLE cvs ADD COLUMN IF NOT EXISTS ville VARCHAR(100);
```

### 3. Redémarrer le Backend

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

## 🚀 Utilisation

1. **Accédez au Dashboard** (`/dashboard`)

2. **Uploadez un CV** :
   - Glissez-déposez un fichier PDF ou une image
   - Ou cliquez pour sélectionner un fichier

3. **Attendez l'extraction** :
   - Un loader s'affiche pendant l'extraction
   - Cela peut prendre quelques secondes

4. **Vérifiez les données extraites** :
   - Un formulaire apparaît avec les informations détectées
   - Vérifiez chaque champ
   - Corrigez si nécessaire
   - Ajoutez ou supprimez des compétences

5. **Confirmez** :
   - Cliquez sur "Confirmer et Enregistrer"
   - Les données sont sauvegardées dans la base de données

6. **Continuez l'analyse** :
   - Sélectionnez une offre d'emploi
   - Cliquez sur "Analyser le matching"

## 🔧 Architecture Technique

### Backend

**Service d'Extraction (`backend/app/services/cv_extractor.py`)** :
- Classe `CVExtractor` avec méthodes pour PDF et images
- Extraction par expressions régulières et heuristiques
- Détection de patterns (email, téléphone, villes marocaines)
- Extraction de compétences techniques courantes

**API (`backend/app/api/cvs.py`)** :
- `POST /api/cvs/upload` : Upload et extraction
- `PUT /api/cvs/{cv_id}/update-data` : Mise à jour des données vérifiées

**Schémas Pydantic** :
- `CVExtractedData` : Structure des données extraites
- `CVUploadResponse` : Réponse avec données extraites
- `CVUpdateData` : Données vérifiées par l'utilisateur

### Frontend

**Composant de Vérification (`components/dashboard/cv-verification-form.tsx`)** :
- Formulaire React avec tous les champs éditables
- Gestion des compétences (ajout/suppression)
- Validation et soumission
- Messages de confirmation

**Page Dashboard (`app/dashboard/page.tsx`)** :
- Workflow complet d'upload → vérification → enregistrement
- États de chargement
- Gestion des erreurs avec toasts

## 📝 Améliorations Futures Possibles

1. **IA/ML pour l'extraction** :
   - Utiliser des modèles NLP pré-entraînés
   - Extraction plus précise des expériences et formations
   - Reconnaissance d'entités nommées (NER)

2. **Support de plus de formats** :
   - DOCX (Word)
   - HTML
   - LinkedIn PDF

3. **Extraction multilingue** :
   - Support de plus de langues avec OCR
   - Détection automatique de la langue

4. **Suggestions intelligentes** :
   - Proposer des compétences manquantes
   - Normalisation automatique (formats de téléphone, villes)

## ⚠️ Notes Importantes

- **Performance** : L'extraction peut prendre 2-5 secondes selon la taille du fichier
- **OCR** : L'extraction depuis images dépend de la qualité de l'image
- **Précision** : Les données extraites ne sont pas garanties à 100% - d'où la vérification
- **Langues** : L'extraction fonctionne mieux avec du texte en français ou anglais

## 🐛 Dépannage

### Erreur "pytesseract not found"
- Assurez-vous que Tesseract OCR est installé sur le système
- Vérifiez que le chemin est dans le PATH

### Extraction incomplète
- Vérifiez la qualité du CV (PDF natif vs scanné)
- Les CV très stylisés peuvent avoir une extraction limitée
- Utilisez le formulaire de vérification pour compléter manuellement

### Erreur lors de l'upload
- Vérifiez que le backend est bien démarré
- Vérifiez les logs du backend pour plus de détails
- Assurez-vous que le dossier `uploads/cvs` existe

## 📚 Ressources

- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [Pytesseract GitHub](https://github.com/madmaze/pytesseract)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

---

**Développé pour SmartHire** - Votre assistant intelligent pour la recherche d'emploi ! 🚀

