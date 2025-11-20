from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AlertBase(BaseModel):
    nom: str
    poste_keywords: str
    ville: Optional[str]
    type_contrat: Optional[str]
    salaire_min: Optional[int]
    competences: Optional[List[str]]
    frequence: str

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    nom: Optional[str]
    poste_keywords: Optional[str]
    ville: Optional[str]
    type_contrat: Optional[str]
    salaire_min: Optional[int]
    competences: Optional[List[str]]
    frequence: Optional[str]
    active: Optional[bool]

class AlertResponse(AlertBase):
    id: int
    user_id: int
    active: bool
    offres_trouvees: int
    last_check: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


