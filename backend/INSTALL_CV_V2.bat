@echo off
echo ============================================
echo Installation du CV Extractor V2
echo ============================================
echo.

echo [1/3] Installation des dependances Python...
pip install pdfplumber==0.10.3 python-dateutil==2.8.2 rapidfuzz==3.5.2 spacy==3.7.2
if %errorlevel% neq 0 (
    echo ERREUR: Installation des dependances echouee
    pause
    exit /b 1
)

echo.
echo [2/3] Installation du modele SpaCy francais...
python -m spacy download fr_core_news_sm
if %errorlevel% neq 0 (
    echo ERREUR: Installation du modele SpaCy echouee
    pause
    exit /b 1
)

echo.
echo [3/3] Installation de pdf2image (optionnel pour OCR avance)...
pip install pdf2image
if %errorlevel% neq 0 (
    echo AVERTISSEMENT: pdf2image non installe (optionnel)
)

echo.
echo ============================================
echo Installation terminee avec succes!
echo ============================================
echo.
echo Vous pouvez maintenant utiliser le CV Extractor V2
echo Pour demarrer le serveur: START_SERVER.bat
echo.
pause

