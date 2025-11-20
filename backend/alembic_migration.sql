-- Migration pour ajouter les nouveaux champs à la table users
-- Exécuter ce script dans PostgreSQL

-- Se connecter à la base de données smarthire_db
-- psql -U postgres -d smarthire_db

-- Ajouter les colonnes pour les préférences d'emploi
ALTER TABLE users ADD COLUMN IF NOT EXISTS salaire_minimum INTEGER;
ALTER TABLE users ADD COLUMN IF NOT EXISTS type_contrat_prefere VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS secteur_activite VARCHAR(100);
ALTER TABLE users ADD COLUMN IF NOT EXISTS accepte_teletravail BOOLEAN DEFAULT FALSE;

-- Vérifier que les colonnes ont été ajoutées
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'users'
ORDER BY ordinal_position;

