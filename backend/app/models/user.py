from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from ..database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    mot_de_passe = Column(String(255), nullable=False)
    telephone = Column(String(20), nullable=True)
    photo_profil = Column(String(255), nullable=True)
    ville_preferee = Column(String(100), nullable=True)
    
    # Nouveaux champs pour les préférences d'emploi
    salaire_minimum = Column(Integer, nullable=True)  # Salaire minimum en MAD
    type_contrat_prefere = Column(String(50), nullable=True)  # CDI, CDD, Stage, Freelance
    secteur_activite = Column(String(100), nullable=True)  # Informatique, Finance, etc.
    accepte_teletravail = Column(Boolean, default=False)  # Accepte le télétravail
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
