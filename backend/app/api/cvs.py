from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import time
from ..database import get_db
from ..models.user import User
from ..models.cv import CV
from ..schemas.cv import CVResponse, CVUploadResponse, CVExtractedData, CVUpdateData
from ..core.deps import get_current_user
from ..config import settings
from ..services.cv_extractor import CVExtractor

router = APIRouter(prefix="/api/cvs", tags=["CVs"])

ALLOWED_CV_TYPES = {"application/pdf", "image/jpeg", "image/jpg", "image/png"}


@router.post("/upload", response_model=CVUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a CV file and extract data for verification"""
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
    
    # Extract data from CV
    extractor = CVExtractor()
    if type_fichier == "pdf":
        extracted_data = extractor.extract_from_pdf(file_path)
    else:
        extracted_data = extractor.extract_from_image(file_path)
    
    # Create CV entry in database with temporary data
    new_cv = CV(
        user_id=current_user.id,
        nom_fichier=file.filename,
        type_fichier=type_fichier,
        chemin_fichier=filename,
        contenu_texte=extracted_data.get("contenu_texte", ""),
        competences_extraites=extracted_data.get("competences", [])
    )
    
    db.add(new_cv)
    db.commit()
    db.refresh(new_cv)
    
    # Return CV with extracted data for verification
    return {
        "id": new_cv.id,
        "extracted_data": CVExtractedData(**extracted_data)
    }


@router.put("/{cv_id}/update-data", response_model=CVResponse)
def update_cv_data(
    cv_id: int,
    cv_data: CVUpdateData,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update CV data after user verification"""
    # Get CV and verify ownership
    cv = db.query(CV).filter(CV.id == cv_id, CV.user_id == current_user.id).first()
    
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV not found or you don't have permission to update it"
        )
    
    # Update CV with verified data
    if cv_data.nom_complet:
        cv.nom_complet = cv_data.nom_complet
    if cv_data.email_cv:
        cv.email_cv = cv_data.email_cv
    if cv_data.telephone_cv:
        cv.telephone_cv = cv_data.telephone_cv
    if cv_data.ville:
        cv.ville = cv_data.ville
    if cv_data.competences_extraites:
        cv.competences_extraites = cv_data.competences_extraites
    
    db.commit()
    db.refresh(cv)
    
    return cv


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


