from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse, JobSearchParams

router = APIRouter()

@router.post("/", response_model=JobResponse)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    new_job = Job(**job_data.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/search", response_model=List[JobResponse])
def search_jobs(
    poste: Optional[str] = Query(None),
    ville: Optional[str] = Query(None),
    type_contrat: Optional[str] = Query(None),
    salaire_min: Optional[int] = Query(None),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    query = db.query(Job)
    
    if poste:
        query = query.filter(Job.titre.ilike(f"%{poste}%"))
    if ville:
        query = query.filter(Job.ville == ville)
    if type_contrat:
        query = query.filter(Job.type_contrat == type_contrat)
    if salaire_min:
        query = query.filter(Job.salaire_min >= salaire_min)
    
    jobs = query.limit(limit).all()
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/", response_model=List[JobResponse])
def get_all_jobs(
    skip: int = Query(0),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs


