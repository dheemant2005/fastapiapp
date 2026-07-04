from fastapi import APIRouter, HTTPException, Depends, status
from schemas.job import JobCreate, JobUpdate, JobResponse
from models.job import Job
from sqlalchemy.orm import Session
from database import get_db
from utils.oauth2 import get_current_user,role_required

router = APIRouter(prefix="/job", tags=["job"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db), current_user=Depends(role_required(["admin"]))):
    pass

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[JobResponse])
def get_all_job(db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    jobs = db.query(Job).all()
    return jobs

@router.get("/{job_id}", status_code=status.HTTP_200_OK, response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

@router.put("/{job_id}", status_code=status.HTTP_200_OK, response_model=JobResponse)
def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    job_data = job.dict(exclude_unset=True)
    for key, value in job_data.items():
        setattr(db_job, key, value)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return None

# @router.get("/")
# def read_job():
#     return {"job": "Job root"}

# @router.get("/{job_id}")
# def read_job(job_id: int):
#     return {"job_id": job_id}