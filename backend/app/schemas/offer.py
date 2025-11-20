from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class OfferResponse(BaseModel):
    id: int
    titre: str
    entreprise: Optional[str] = None
    description: str
    localisation: Optional[str] = None
    ville: Optional[str] = None
    type_contrat: Optional[str] = None
    salaire: Optional[str] = None
    url_source: str
    source_site: str
    date_publication: Optional[date] = None
    competences_requises: Optional[List[str]] = None
    competences_souhaitees: Optional[List[str]] = None
    est_active: bool
    date_scraping: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class OfferSearch(BaseModel):
    ville: Optional[str] = None
    type_contrat: Optional[str] = None
    competences: Optional[List[str]] = None


