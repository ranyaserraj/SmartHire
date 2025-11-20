from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

class AnalysisCreate(BaseModel):
    cv_id: int
    job_id: int

class AnalysisResponse(BaseModel):
    id: int
    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    suggestions: List[Dict]
    ats_keywords: List[str]
    acceptance_probability: float
    created_at: datetime
    
    class Config:
        from_attributes = True


