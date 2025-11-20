from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.user import User
from app.models.cv import CV
from app.models.analysis import Analysis
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/stats")
def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Compter les CVs uploadés
    total_cvs = db.query(func.count(CV.id)).filter(CV.user_id == current_user.id).scalar()
    
    # Compter les analyses effectuées
    total_analyses = db.query(func.count(Analysis.id)).filter(Analysis.user_id == current_user.id).scalar()
    
    # Meilleur score
    best_score = db.query(func.max(Analysis.overall_score)).filter(Analysis.user_id == current_user.id).scalar()
    
    # Score moyen
    avg_score = db.query(func.avg(Analysis.overall_score)).filter(Analysis.user_id == current_user.id).scalar()
    
    return {
        "totalCVs": total_cvs or 0,
        "totalAnalyses": total_analyses or 0,
        "bestScore": round(best_score, 1) if best_score else 0,
        "avgScore": round(avg_score, 1) if avg_score else 0
    }


