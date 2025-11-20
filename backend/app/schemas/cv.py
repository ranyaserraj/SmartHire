from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class CVUpload(BaseModel):
    user_id: int
    nom_fichier: str
    type_fichier: str


class CVExtractedData(BaseModel):
    """Données extraites du CV à vérifier par l'utilisateur"""
    nom_complet: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    ville: Optional[str] = None
    competences: List[str] = []
    experience: List[Dict[str, Any]] = []
    formation: List[Dict[str, Any]] = []
    langues: List[str] = []
    contenu_texte: str = ""


class CVUploadResponse(BaseModel):
    """Réponse après upload du CV avec données extraites"""
    id: int
    extracted_data: CVExtractedData
    
    class Config:
        from_attributes = True


class CVUpdateData(BaseModel):
    """Données vérifiées et corrigées par l'utilisateur"""
    cv_id: int
    nom_complet: Optional[str] = None
    email_cv: Optional[str] = None
    telephone_cv: Optional[str] = None
    ville: Optional[str] = None
    competences_extraites: List[str] = []


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
