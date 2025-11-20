from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import time
from ..database import get_db
from ..models.user import User
from ..models.cv import CV
from ..schemas.cv import CVResponse
from ..core.deps import get_current_user
from ..config import settings

router = APIRouter(prefix="/api/cvs", tags=["CVs"])

ALLOWED_CV_TYPES = {"application/pdf", "image/jpeg", "image/jpg", "image/png"}


@router.post("/upload", response_model=CVResponse, status_code=status.HTTP_201_CREATED)
async def upload_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a CV file"""
    # Validate file type
    if file.content_type not in ALLOWED_CV_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and image files are allowed"
        )
    
    # Read file and validate size
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size must be less than {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )
    
    # Determine file type
    extension = file.filename.split(".")[-1].lower()
    if extension == "pdf":
        type_fichier = "pdf"
    elif extension in ["jpg", "jpeg"]:
        type_fichier = "jpg"
    elif extension == "png":
        type_fichier = "png"
    else:
        type_fichier = extension
    
    # Generate unique filename
    filename = f"{current_user.id}_{int(time.time())}.{extension}"
    file_path = os.path.join(settings.CV_DIR, filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Create CV entry in database
    new_cv = CV(
        user_id=current_user.id,
        nom_fichier=file.filename,
        type_fichier=type_fichier,
        chemin_fichier=filename,
        contenu_texte="",  # Will be extracted later with OCR/PDF parser
        competences_extraites=[]
    )
    
    db.add(new_cv)
    db.commit()
    db.refresh(new_cv)
    
    return new_cv


@router.get("/me", response_model=List[CVResponse])
def get_my_cvs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all CVs of the current user"""
    cvs = db.query(CV).filter(CV.user_id == current_user.id).order_by(CV.created_at.desc()).all()
    return cvs


@router.delete("/{cv_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cv(
    cv_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a CV"""
    # Get CV and verify ownership
    cv = db.query(CV).filter(CV.id == cv_id, CV.user_id == current_user.id).first()
    
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found or you don't have permission to delete it"
        )
    
    # Delete physical file
    file_path = os.path.join(settings.CV_DIR, cv.chemin_fichier)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete from database
    db.delete(cv)
    db.commit()
    
    return None


