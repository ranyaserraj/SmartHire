@echo off
echo ===============================================
echo   DEMARRAGE SERVEUR FASTAPI - SMARTHIRE
echo ===============================================
echo.

REM Activer l'environnement virtuel si il existe
if exist "venv\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call venv\Scripts\activate.bat
) else (
    echo Pas d'environnement virtuel detecte.
)

echo.
echo Demarrage du serveur sur http://localhost:8080
echo Documentation: http://localhost:8080/docs
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.
echo ===============================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

