-- Script pour vérifier les données utilisateur en base
-- Exécuter : psql -U postgres -d smarthire_db -f test_user_data.sql

-- Mot de passe : ranyaa

-- Afficher tous les utilisateurs avec TOUTES leurs informations
SELECT 
    id,
    prenom,
    nom,
    email,
    telephone,
    ville_preferee,
    photo_profil,
    salaire_minimum,
    type_contrat_prefere,
    secteur_activite,
    accepte_teletravail,
    created_at,
    updated_at
FROM users
ORDER BY id DESC
LIMIT 5;

-- Afficher spécifiquement les préférences d'emploi
SELECT 
    id,
    prenom,
    nom,
    email,
    '---' as separator,
    ville_preferee as "Ville préférée",
    salaire_minimum as "Salaire min",
    type_contrat_prefere as "Type contrat",
    secteur_activite as "Secteur",
    accepte_teletravail as "Télétravail"
FROM users
WHERE email = 'hind@gmail.com'  -- Remplacer par votre email
ORDER BY id DESC;

-- Vérifier si les colonnes existent
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'users'
  AND column_name IN ('salaire_minimum', 'type_contrat_prefere', 'secteur_activite', 'accepte_teletravail')
ORDER BY column_name;

