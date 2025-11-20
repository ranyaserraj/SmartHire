from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cv_id = Column(Integer, ForeignKey("cvs.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    
    # Scores de matching
    overall_score = Column(Float)  # Score global 0-100
    skills_score = Column(Float)
    experience_score = Column(Float)
    education_score = Column(Float)
    
    # Résultats détaillés
    matching_skills = Column(JSON)  # Compétences correspondantes
    missing_skills = Column(JSON)  # Compétences manquantes
    suggestions = Column(JSON)  # Suggestions d'amélioration
    ats_keywords = Column(JSON)  # Mots-clés ATS
    
    # Prédiction IA
    acceptance_probability = Column(Float)  # Probabilité d'être accepté
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="analyses")
    cv = relationship("CV", back_populates="analyses")
    job = relationship("Job")


