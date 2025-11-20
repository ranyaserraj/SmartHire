@echo off
echo Création du fichier .env avec mot de passe PostgreSQL: ranyaa
echo.

(
echo DATABASE_URL=postgresql://postgres:ranyaa@localhost:5432/smarthire_db
echo SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=1440
echo.
echo UPLOAD_DIR=./uploads
echo AVATAR_DIR=./uploads/avatars
echo CV_DIR=./uploads/cvs
echo MAX_UPLOAD_SIZE=10485760
echo.
echo SCRAPING_ENABLED=true
echo SCRAPING_MAX_OFFERS=50
) > .env

echo ✓ Fichier .env créé avec succès!
echo ✓ Mot de passe PostgreSQL configuré: ranyaa
echo.
echo Vous pouvez maintenant démarrer le serveur avec:
echo   uvicorn app.main:app --reload
echo.
pause


