from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class CVUpload(BaseModel):
    user_id: int
    nom_fichier: str
    type_fichier: str


class CVResponse(BaseModel):
    id: int
    user_id: int
    nom_fichier: str
    type_fichier: str
    chemin_fichier: str
    contenu_texte: str
    nom_complet: Optional[str] = None
    email_cv: Optional[str] = None
    telephone_cv: Optional[str] = None
    competences_extraites: Optional[List[str]] = None
    date_upload: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
