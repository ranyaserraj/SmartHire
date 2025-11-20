from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from app.db.base import Base

class CoverLetter(Base):
    __tablename__ = "cover_letters"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    
    # 3 versions
    formal_version = Column(Text)
    dynamic_version = Column(Text)
    creative_version = Column(Text)
    
    # Email d'accompagnement
    email_subject = Column(String)
    email_body = Column(Text)
    
    # Préparation entretien
    interview_questions = Column(Text)  # JSON stringifié
    
    created_at = Column(DateTime, default=datetime.utcnow)


