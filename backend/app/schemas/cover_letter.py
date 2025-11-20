from pydantic import BaseModel
from typing import List, Dict

class CoverLetterCreate(BaseModel):
    analysis_id: int

class CoverLetterResponse(BaseModel):
    id: int
    formal_version: str
    dynamic_version: str
    creative_version: str
    email_subject: str
    email_body: str
    interview_questions: List[Dict]
    
    class Config:
        from_attributes = True


