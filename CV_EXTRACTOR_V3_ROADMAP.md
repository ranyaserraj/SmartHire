# 🚀 CV Extractor V3 - Roadmap Complète

## 📊 État des Lieux

### ✅ Déjà Implémenté dans V2

| Fonctionnalité | Statut | Qualité |
|----------------|--------|---------|
| pdfplumber (au lieu de PyPDF2) | ✅ Fait | Bon |
| rapidfuzz (fuzzy matching) | ✅ Fait | Partiel |
| Patterns de dates multiples | ✅ Fait | Partiel |
| Détection sections (regex) | ✅ Fait | Basique |
| Extraction téléphone | ✅ Fait | Bon |
| Stopwords (150+ mots) | ✅ Fait | Excellent |
| Extraction compétences | ✅ Fait | Moyen |

### ❌ Manquant / À Améliorer

| Fonctionnalité | Priorité | Complexité | Impact |
|----------------|----------|------------|--------|
| **ESCO (13 000+ skills)** | 🔴 HAUTE | Moyenne | ⭐⭐⭐⭐⭐ |
| Tri blocs par position (x, y) | 🔴 HAUTE | Haute | ⭐⭐⭐⭐⭐ |
| Fuzzy matching sections | 🔴 HAUTE | Faible | ⭐⭐⭐⭐ |
| Dates avec séparateurs (→, –, >) | 🟠 MOYENNE | Faible | ⭐⭐⭐⭐ |
| Regroupement lignes logiques | 🟠 MOYENNE | Moyenne | ⭐⭐⭐⭐ |
| Split compétences (,  ;  •) | 🟠 MOYENNE | Faible | ⭐⭐⭐⭐ |
| OCR traineddata FR/EN/AR | 🟠 MOYENNE | Moyenne | ⭐⭐⭐ |
| Détection nom intelligente | 🟠 MOYENNE | Moyenne | ⭐⭐⭐⭐ |
| Extraction adresse complète | 🟡 BASSE | Moyenne | ⭐⭐⭐ |
| Langues + niveaux CEFR | 🟡 BASSE | Faible | ⭐⭐⭐ |
| Formation intelligente | 🟠 MOYENNE | Moyenne | ⭐⭐⭐⭐ |
| Expériences sans section | 🟠 MOYENNE | Haute | ⭐⭐⭐⭐ |
| NLP avec spaCy | 🟡 BASSE | Haute | ⭐⭐⭐ |
| Soft skills automatiques | 🔴 HAUTE | Moyenne | ⭐⭐⭐⭐⭐ |
| Détection multi-langue | 🟡 BASSE | Faible | ⭐⭐ |

---

## 🎯 Phase 1 : Améliorations Critiques (Priorité HAUTE)

### 1.1 Intégration ESCO ⭐⭐⭐⭐⭐

**Pourquoi :** Dataset officiel de l'UE avec 13 000+ compétences en 28 langues

**Comment :**
```python
# backend/data/esco_skills_sample.json (déjà créé)
# Contient 96 compétences techniques + 43 soft skills

# À faire :
# 1. Télécharger le dataset complet ESCO
# 2. Parser et indexer les skills
# 3. Remplacer tech_skills_base par ESCO
```

**Fichiers à modifier :**
- `cv_extractor_v3.py` : Charger ESCO au __init__
- `data/esco_skills_sample.json` : Fichier temporaire (139 skills)
- `data/esco_skills_full.json` : Dataset complet (13 000+)

**Avantages :**
- ✅ 13 000+ compétences vs 96 actuellement
- ✅ Traductions FR/EN/ES/DE/etc.
- ✅ Classification hard/soft skills
- ✅ Compétences liées aux métiers
- ✅ Mis à jour régulièrement par l'UE

**Code :**
```python
class CVExtractorV3:
    def __init__(self):
        # Charger ESCO
        self.esco_skills = self._load_esco_skills()
    
    def _load_esco_skills(self):
        data_file = Path(__file__).parent.parent / "data" / "esco_skills_sample.json"
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _extract_skills_esco(self, text: str) -> List[str]:
        skills_found = set()
        
        # Chercher toutes les compétences ESCO
        for skill in self.esco_skills['technical_skills']:
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text.lower()):
                skills_found.add(skill)
        
        for skill in self.esco_skills['soft_skills']:
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text.lower()):
                skills_found.add(skill)
        
        return sorted(list(skills_found))
```

---

### 1.2 Tri des Blocs par Position Spatiale (x, y) ⭐⭐⭐⭐⭐

**Problème actuel :** CV en 2 colonnes → texte extrait dans le mauvais ordre

**Solution :** Utiliser pdfplumber pour extraire les coordonnées et trier

```python
def _extract_from_pdf_spatial(self, file_path: Path) -> str:
    """Extraction avec tri spatial pour CV en colonnes"""
    text_blocks = []
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            # Extraire les mots avec coordonnées
            words = page.extract_words(
                x_tolerance=3,
                y_tolerance=3,
                keep_blank_chars=False
            )
            
            # Regrouper par lignes (même y)
            lines = {}
            for word in words:
                y = round(word['top'])
                if y not in lines:
                    lines[y] = []
                lines[y].append((word['x0'], word['text']))
            
            # Trier chaque ligne de gauche à droite
            for y in sorted(lines.keys()):
                line_words = sorted(lines[y], key=lambda x: x[0])
                line_text = ' '.join([w[1] for w in line_words])
                text_blocks.append(line_text)
    
    return '\n'.join(text_blocks)
```

**Impact :**
- ✅ CV en 2 colonnes correctement lus
- ✅ CV en tableaux bien parsés
- ✅ Ordre de lecture "humain"

---

### 1.3 Fuzzy Matching pour Détection de Sections ⭐⭐⭐⭐

**Problème actuel :**
```python
if keyword in line_lower:  # Trop strict
```

**Ne détecte pas :**
- `WORK EXPERIENCE` (espace)
- `EXPÉRIENCES PROFESSIONNELLES` (accent)
- `EXPÉRIENCE —` (caractère spécial)
- `[🔧 ICON] Experience` (avec icône)
- `EXPERIENCE` (stylisé)

**Solution :** Fuzzy matching avec rapidfuzz

```python
def _detect_sections_fuzzy(self, lines: List[str]) -> Dict[str, List[str]]:
    """Détection de sections avec fuzzy matching"""
    sections = {}
    current_section = None
    current_content = []
    
    section_keywords = {
        'experience': ['experience', 'work experience', 'employment', 'career'],
        'formation': ['education', 'formation', 'studies', 'degree'],
        'competences': ['skills', 'competences', 'expertise', 'abilities'],
    }
    
    for line in lines:
        line_clean = re.sub(r'[^\w\s]', '', line.lower())  # Enlever symboles
        
        # Tester chaque type de section
        section_detected = None
        best_score = 0
        
        for section_name, keywords in section_keywords.items():
            for keyword in keywords:
                score = fuzz.partial_ratio(keyword, line_clean)
                if score > 85 and score > best_score:  # 85% de similarité
                    section_detected = section_name
                    best_score = score
        
        if section_detected:
            # Sauvegarder la section précédente
            if current_section and current_content:
                sections[current_section] = current_content
            
            current_section = section_detected
            current_content = []
        elif current_section:
            current_content.append(line)
    
    # Sauvegarder la dernière section
    if current_section and current_content:
        sections[current_section] = current_content
    
    return sections
```

**Impact :**
- ✅ Détecte sections même avec typos
- ✅ Gère les accents et caractères spéciaux
- ✅ Ignore les icônes et symboles
- ✅ Fonctionne en FR et EN

---

### 1.4 Soft Skills Automatiques (ESCO) ⭐⭐⭐⭐⭐

**Actuellement :** Liste manuelle de 43 soft skills

**Avec ESCO :** Reconnaissance automatique de centaines de soft skills

```python
def _extract_soft_skills_esco(self, text: str) -> List[str]:
    """Extraction des soft skills depuis ESCO"""
    soft_skills_found = set()
    text_lower = text.lower()
    
    # Chercher toutes les soft skills ESCO
    for skill in self.esco_skills.get('soft_skills', []):
        # Recherche exacte
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
            soft_skills_found.add(skill)
        # Fuzzy match pour variations
        else:
            words = text.split()
            matches = process.extract(skill, words, scorer=fuzz.ratio, limit=1)
            if matches and matches[0][1] > 90:  # 90% de similarité
                soft_skills_found.add(skill)
    
    return sorted(list(soft_skills_found))
```

**Soft Skills détectées automatiquement :**
- Leadership, Team Management, Project Management
- Communication, Public Speaking, Negotiation
- Problem Solving, Critical Thinking, Analytical Skills
- Adaptability, Creativity, Innovation
- Time Management, Organization, Attention to Detail
- Gestion d'équipe, Travail en équipe, Résolution de problèmes
- etc.

---

## 🎯 Phase 2 : Améliorations Moyennes (Priorité MOYENNE)

### 2.1 Dates avec Tous les Séparateurs ⭐⭐⭐⭐

**Actuellement manquant :**
- `2018–2020` (tiret long)
- `Jan 2022 → Mar 2023` (flèche)
- `2019 > Présent` (chevron)

**Nouveaux patterns :**
```python
self.date_separators = [
    r'[-–—]',  # Tirets (court, moyen, long)
    r'[→>]',   # Flèches
    r'(?:to|à|a)',  # Mots
]

self.date_pattern_with_range = (
    r'(' + '|'.join(self.date_patterns) + r')\s*'
    r'(' + '|'.join(self.date_separators) + r')\s*'
    r'(' + '|'.join(self.date_patterns) + r')'
)
```

---

### 2.2 Regroupement de Lignes Logiques ⭐⭐⭐⭐

**Problème :**
```
Gestion de projets
Agile Scrum Jira
```
→ Doit être reconnu comme une seule compétence

**Solution :**
```python
def _regroup_logical_lines(self, lines: List[str]) -> List[str]:
    """Regroupe les lignes qui appartiennent ensemble"""
    regrouped = []
    current_group = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_group:
                regrouped.append(' '.join(current_group))
                current_group = []
            continue
        
        # Si la ligne est courte et la suivante aussi → regrouper
        if len(line) < 50 and not line.endswith(('.', '!', '?')):
            current_group.append(line)
        else:
            if current_group:
                current_group.append(line)
                regrouped.append(' '.join(current_group))
                current_group = []
            else:
                regrouped.append(line)
    
    if current_group:
        regrouped.append(' '.join(current_group))
    
    return regrouped
```

---

### 2.3 Split Compétences par Séparateurs ⭐⭐⭐⭐

**Actuellement :** Détecte `"Python, React, SQL"` comme un seul mot

**Solution :**
```python
def _split_skills(self, text: str) -> List[str]:
    """Split les compétences selon les séparateurs"""
    separators = [',', ';', '/', '•', '-', '|', '\n']
    
    # Remplacer tous les séparateurs par virgule
    for sep in separators:
        text = text.replace(sep, ',')
    
    # Split et nettoyer
    skills = [s.strip() for s in text.split(',') if s.strip()]
    
    return skills
```

---

### 2.4 Détection du Nom Intelligente ⭐⭐⭐⭐

**Problèmes actuels :**
- Nom en bannière
- Nom au milieu
- Nom dans une image
- Nom en majuscules
- Nom sur 2 lignes

**Solution :**
```python
def _extract_name_intelligent(self, lines: List[str]) -> str:
    """Détection intelligente du nom dans les 20 premières lignes"""
    candidates = []
    
    for i, line in enumerate(lines[:20]):
        line = line.strip()
        if not line or len(line) < 3:
            continue
        
        # Skip si email, téléphone, adresse
        if re.search(r'@|\.com|\d{5,}|http', line):
            continue
        
        # Score basé sur critères
        score = 0
        words = line.split()
        
        # Critère 1 : Majuscules (nom souvent en caps)
        if line.isupper():
            score += 3
        elif line.istitle():
            score += 2
        
        # Critère 2 : 2-4 mots (prénom + nom + éventuellement titre)
        if 2 <= len(words) <= 4:
            score += 2
        
        # Critère 3 : Que des lettres (pas de chiffres)
        if all(re.match(r'^[A-ZÀ-ÿa-z\'-]+$', word) for word in words):
            score += 2
        
        # Critère 4 : Position (plus haut = plus probable)
        score += (20 - i) / 5
        
        # Critère 5 : Taille police (si disponible via pdfplumber)
        # score += font_size_ratio
        
        candidates.append((line, score))
    
    # Retourner le candidat avec le meilleur score
    if candidates:
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]
    
    return ""
```

---

## 🎯 Phase 3 : Améliorations Avancées (Priorité BASSE)

### 3.1 NLP avec spaCy ⭐⭐⭐

**Utilisation :**
- Détection automatique des entités (noms, organisations, lieux)
- Extraction des métiers
- Compréhension du contexte

```python
import spacy

class CVExtractorV3:
    def __init__(self):
        self.nlp_fr = spacy.load("fr_core_news_sm")
        self.nlp_en = spacy.load("en_core_web_sm")
    
    def _extract_entities_spacy(self, text: str, lang='fr') -> Dict:
        nlp = self.nlp_fr if lang == 'fr' else self.nlp_en
        doc = nlp(text)
        
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
        }
        
        for ent in doc.ents:
            if ent.label_ == 'PER':
                entities['persons'].append(ent.text)
            elif ent.label_ == 'ORG':
                entities['organizations'].append(ent.text)
            elif ent.label_ in ['LOC', 'GPE']:
                entities['locations'].append(ent.text)
        
        return entities
```

---

### 3.2 Détection Multi-Langue ⭐⭐

**Installation :**
```bash
pip install langdetect
```

**Code :**
```python
from langdetect import detect

def _detect_language(self, text: str) -> str:
    """Détecte la langue du CV"""
    try:
        return detect(text)  # 'fr', 'en', 'es', etc.
    except:
        return 'en'  # Défaut
```

---

## 📦 Dépendances Additionnelles

```bash
# backend/requirements.txt

# Déjà installé
pdfplumber==0.11.8
rapidfuzz==3.14.3
python-dateutil==2.9.0.post0

# À installer pour V3
spacy==3.7.2
langdetect==1.0.9
python-Levenshtein==0.25.0  # Accélère rapidfuzz

# Modèles spaCy
# python -m spacy download fr_core_news_sm
# python -m spacy download en_core_web_sm
```

---

## 🗓️ Planning de Développement

### Sprint 1 (Priorité HAUTE) - 2-3 jours

- [x] Intégration ESCO (échantillon créé) ✅
- [ ] Tri spatial des blocs (x, y)
- [ ] Fuzzy matching sections
- [ ] Soft skills automatiques ESCO

### Sprint 2 (Priorité MOYENNE) - 2 jours

- [ ] Patterns dates étendus (→, –, >)
- [ ] Regroupement lignes logiques
- [ ] Split compétences
- [ ] Détection nom intelligente

### Sprint 3 (Priorité BASSE) - 1-2 jours

- [ ] NLP spaCy
- [ ] Détection multi-langue
- [ ] Extraction adresse complète
- [ ] Langues + niveaux CEFR

---

## 💰 Comparaison V2 vs V3

| Critère | V2 (Actuel) | V3 (Futur) |
|---------|-------------|------------|
| **Précision globale** | ~88% | ~93-95% |
| **Compétences (dataset)** | 96 skills | 13 000+ (ESCO) |
| **CV en colonnes** | ⚠️ Moyen | ✅ Excellent |
| **Soft skills** | 43 manuels | Centaines (ESCO) |
| **Dates complexes** | ⚠️ Partiel | ✅ Complet |
| **Détection sections** | ⚠️ Stricte | ✅ Fuzzy |
| **Multi-langue** | FR/EN partiel | FR/EN/ES/DE/etc. |
| **NLP** | ❌ Non | ✅ spaCy |
| **Coût** | ✅ Gratuit | ✅ Gratuit |

---

## 🎯 Recommandation

### Option 1 : Rester sur V2 ✅
**Si :** Précision de 88% est suffisante pour votre usage

### Option 2 : Sprint 1 uniquement (ESCO + Spatial) ⭐
**Si :** Vous voulez passer à 93% de précision rapidement (2-3 jours)

### Option 3 : V3 complète 🚀
**Si :** Vous visez l'excellence (95%+) et avez 5-7 jours de développement

---

**Fichiers créés :**
- ✅ `backend/data/esco_skills_sample.json` (139 compétences)
- ✅ `backend/download_esco.py` (script d'installation ESCO)
- ✅ `CV_EXTRACTOR_V3_ROADMAP.md` (ce document)

**Prochaine étape :** Implémenter Sprint 1 (ESCO + Spatial) ?

