from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    cv_id = Column(Integer, ForeignKey("cvs.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    ml_score = Column(Float)  # Score ML de recommandation
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    job = relationship("Job", back_populates="matches")


