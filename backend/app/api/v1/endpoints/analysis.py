from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.models.cv import CV
from app.models.job import Job
from app.schemas.analysis import AnalysisCreate, AnalysisResponse
from app.core.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=AnalysisResponse)
def create_analysis(
    analysis_data: AnalysisCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que le CV appartient à l'utilisateur
    cv = db.query(CV).filter(CV.id == analysis_data.cv_id, CV.user_id == current_user.id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    
    # Vérifier que le job existe
    job = db.query(Job).filter(Job.id == analysis_data.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Créer l'analyse (ici simplifié, normalement on appelle les services d'analyse)
    new_analysis = Analysis(
        user_id=current_user.id,
        cv_id=analysis_data.cv_id,
        job_id=analysis_data.job_id,
        overall_score=85.0,
        skills_score=80.0,
        experience_score=90.0,
        education_score=85.0,
        matching_skills=["Python", "React", "SQL"],
        missing_skills=["Docker", "Kubernetes"],
        suggestions=[
            {"priority": "high", "text": "Ajouter Docker dans les compétences"},
            {"priority": "medium", "text": "Quantifier vos réalisations"}
        ],
        ats_keywords=["Python", "React", "Full Stack"],
        acceptance_probability=78.5
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    
    return new_analysis

@router.get("/", response_model=List[AnalysisResponse])
def get_user_analyses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    analyses = db.query(Analysis).filter(Analysis.user_id == current_user.id).all()
    return analyses

@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


