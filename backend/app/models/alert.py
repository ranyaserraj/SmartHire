from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    nom = Column(String)
    
    # Critères de recherche
    poste_keywords = Column(String)
    ville = Column(String)
    type_contrat = Column(String)
    salaire_min = Column(Integer)
    competences = Column(JSON)
    
    # Configuration
    frequence = Column(String)  # quotidienne, hebdomadaire
    active = Column(Boolean, default=True)
    
    # Stats
    offres_trouvees = Column(Integer, default=0)
    last_check = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="alerts")


