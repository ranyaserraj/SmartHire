from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import os
import time
from ..database import get_db
from ..models.user import User
from ..schemas.user import UserResponse, UserUpdate
from ..core.deps import get_current_user
from ..config import settings

router = APIRouter(prefix="/api/users", tags=["Users"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB


@router.put("/profile", response_model=UserResponse)
def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    # Update only provided fields
    if user_update.nom is not None:
        current_user.nom = user_update.nom
    if user_update.prenom is not None:
        current_user.prenom = user_update.prenom
    if user_update.telephone is not None:
        current_user.telephone = user_update.telephone
    if user_update.ville_preferee is not None:
        current_user.ville_preferee = user_update.ville_preferee
    if user_update.salaire_minimum is not None:
        current_user.salaire_minimum = user_update.salaire_minimum
    if user_update.type_contrat_prefere is not None:
        current_user.type_contrat_prefere = user_update.type_contrat_prefere
    if user_update.secteur_activite is not None:
        current_user.secteur_activite = user_update.secteur_activite
    if user_update.accepte_teletravail is not None:
        current_user.accepte_teletravail = user_update.accepte_teletravail
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.post("/photo", response_model=UserResponse)
async def upload_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload user profile photo"""
    # Validate file type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPG, JPEG, and PNG images are allowed"
        )
    
    # Read file and validate size
    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image size must be less than 5MB"
        )
    
    # Generate unique filename
    extension = file.filename.split(".")[-1]
    filename = f"{current_user.id}_{int(time.time())}.{extension}"
    file_path = os.path.join(settings.AVATAR_DIR, filename)
    
    # Delete old photo if exists
    if current_user.photo_profil:
        old_path = os.path.join(settings.AVATAR_DIR, current_user.photo_profil)
        if os.path.exists(old_path):
            os.remove(old_path)
    
    # Save new photo
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Update database - stocker le chemin relatif pour accès via URL
    current_user.photo_profil = f"/uploads/avatars/{filename}"
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.get("/{user_id}/photo")
def get_user_photo(user_id: int, db: Session = Depends(get_db)):
    """Get user profile photo"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or not user.photo_profil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found"
        )
    
    file_path = os.path.join(settings.AVATAR_DIR, user.photo_profil)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo file not found"
        )
    
    return FileResponse(file_path)


