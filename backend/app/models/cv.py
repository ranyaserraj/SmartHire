from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..database import Base


class CV(Base):
    __tablename__ = "cvs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    nom_fichier = Column(String(255), nullable=False)
    type_fichier = Column(String(10), nullable=False)
    chemin_fichier = Column(String(255), nullable=False)
    contenu_texte = Column(Text, nullable=False, default="")
    nom_complet = Column(String(200), nullable=True)
    email_cv = Column(String(255), nullable=True)
    telephone_cv = Column(String(20), nullable=True)
    ville = Column(String(100), nullable=True)
    competences_extraites = Column(JSONB, nullable=True)
    date_upload = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationship
    user = relationship("User", backref="cvs")
