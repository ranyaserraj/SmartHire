from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.models.cv import CV
from app.schemas.cv import CVResponse
from app.core.deps import get_current_user
import shutil
import os
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploads/cvs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=CVResponse)
async def upload_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Sauvegarder le fichier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{current_user.id}_{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Créer l'entrée dans la base de données
    new_cv = CV(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path
    )
    db.add(new_cv)
    db.commit()
    db.refresh(new_cv)
    
    return new_cv

@router.get("/", response_model=List[CVResponse])
def get_user_cvs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cvs = db.query(CV).filter(CV.user_id == current_user.id).all()
    return cvs

@router.get("/{cv_id}", response_model=CVResponse)
def get_cv(
    cv_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cv = db.query(CV).filter(CV.id == cv_id, CV.user_id == current_user.id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    return cv

@router.delete("/{cv_id}")
def delete_cv(
    cv_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cv = db.query(CV).filter(CV.id == cv_id, CV.user_id == current_user.id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    
    # Supprimer le fichier
    if os.path.exists(cv.file_path):
        os.remove(cv.file_path)
    
    db.delete(cv)
    db.commit()
    
    return {"message": "CV deleted successfully"}


