from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.models.cover_letter import CoverLetter
from app.schemas.cover_letter import CoverLetterCreate, CoverLetterResponse
from app.core.deps import get_current_user
import json

router = APIRouter()

@router.post("/", response_model=CoverLetterResponse)
def generate_cover_letter(
    data: CoverLetterCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que l'analyse appartient à l'utilisateur
    analysis = db.query(Analysis).filter(
        Analysis.id == data.analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Générer les lettres (ici simplifié, normalement on appelle GPT)
    cover_letter = CoverLetter(
        analysis_id=data.analysis_id,
        formal_version="Version formelle de la lettre...",
        dynamic_version="Version dynamique de la lettre...",
        creative_version="Version créative de la lettre...",
        email_subject="Candidature au poste de Développeur",
        email_body="Madame, Monsieur,\n\nVeuillez trouver ci-joint...",
        interview_questions=json.dumps([
            {
                "question": "Parlez-moi de vous",
                "suggestion": "Je suis un développeur passionné..."
            },
            {
                "question": "Pourquoi ce poste?",
                "suggestion": "Je suis intéressé par ce poste car..."
            }
        ])
    )
    
    db.add(cover_letter)
    db.commit()
    db.refresh(cover_letter)
    
    # Parser le JSON pour la réponse
    response_data = {
        "id": cover_letter.id,
        "formal_version": cover_letter.formal_version,
        "dynamic_version": cover_letter.dynamic_version,
        "creative_version": cover_letter.creative_version,
        "email_subject": cover_letter.email_subject,
        "email_body": cover_letter.email_body,
        "interview_questions": json.loads(cover_letter.interview_questions)
    }
    
    return response_data

@router.get("/{analysis_id}", response_model=CoverLetterResponse)
def get_cover_letter(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que l'analyse appartient à l'utilisateur
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    cover_letter = db.query(CoverLetter).filter(
        CoverLetter.analysis_id == analysis_id
    ).first()
    if not cover_letter:
        raise HTTPException(status_code=404, detail="Cover letter not found")
    
    response_data = {
        "id": cover_letter.id,
        "formal_version": cover_letter.formal_version,
        "dynamic_version": cover_letter.dynamic_version,
        "creative_version": cover_letter.creative_version,
        "email_subject": cover_letter.email_subject,
        "email_body": cover_letter.email_body,
        "interview_questions": json.loads(cover_letter.interview_questions)
    }
    
    return response_data


