from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class JobBase(BaseModel):
    titre: str
    entreprise: str
    ville: str
    secteur: Optional[str]
    type_contrat: str
    salaire_min: Optional[int]
    salaire_max: Optional[int]
    description: str
    competences_requises: List[str]
    experience_requise: Optional[int]
    niveau_etudes: Optional[str]

class JobCreate(JobBase):
    source: str = "manual"
    url: Optional[str]

class JobResponse(JobBase):
    id: int
    source: str
    url: Optional[str]
    date_publication: Optional[datetime]
    scraped_at: datetime
    
    class Config:
        from_attributes = True

class JobSearchParams(BaseModel):
    poste: Optional[str]
    ville: Optional[str]
    type_contrat: Optional[str]
    salaire_min: Optional[int]
    competences: Optional[List[str]]


