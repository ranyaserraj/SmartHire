-- Ajouter le champ ville à la table cvs
ALTER TABLE cvs ADD COLUMN IF NOT EXISTS ville VARCHAR(100);

