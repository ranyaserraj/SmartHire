from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    mot_de_passe: str
    telephone: Optional[str] = None
    ville_preferee: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    mot_de_passe: str


class UserResponse(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    telephone: Optional[str] = None
    photo_profil: Optional[str] = None
    ville_preferee: Optional[str] = None
    salaire_minimum: Optional[int] = None
    type_contrat_prefere: Optional[str] = None
    secteur_activite: Optional[str] = None
    accepte_teletravail: Optional[bool] = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    telephone: Optional[str] = None
    ville_preferee: Optional[str] = None
    salaire_minimum: Optional[int] = None
    type_contrat_prefere: Optional[str] = None
    secteur_activite: Optional[str] = None
    accepte_teletravail: Optional[bool] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


