# 🔄 Redémarrer le Serveur

## Le serveur ne trouve pas `pdfplumber` ?

### Solution Rapide

1. **Arrêter le serveur** : Appuyez sur `Ctrl+C` dans le terminal
2. **Relancer** :

```bash
cd C:\Users\pc\Downloads\code\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Pourquoi cette erreur ?

Les dépendances sont installées dans votre environnement utilisateur Python :
- ✅ `pdfplumber` est installé
- ✅ `rapidfuzz` est installé  
- ✅ `python-dateutil` est installé

Mais parfois le serveur en mode `--reload` ne détecte pas les nouveaux imports. Un simple redémarrage résout le problème.

### Vérifier l'installation

```bash
python -c "import pdfplumber; print('✅ pdfplumber OK')"
python -c "import rapidfuzz; print('✅ rapidfuzz OK')"
python -c "import dateutil; print('✅ python-dateutil OK')"
```

### Si ça ne marche toujours pas

Installer dans le répertoire global (nécessite admin) :

```bash
# Ouvrir PowerShell en mode Admin
pip install --upgrade pdfplumber rapidfuzz python-dateutil
```

Ou utiliser un environnement virtuel :

```bash
cd C:\Users\pc\Downloads\code\backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

---

**Note :** Le serveur devrait fonctionner après un simple `Ctrl+C` puis relance !

