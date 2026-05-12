from fastapi import APIRouter, Query, Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app.services.job_scraper import fetch_jobs
from backend.app.services.job_storage import save_jobs_to_db
from backend.app.models.job import Job



router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_jobs(
    search: str = Query(default="python"),
    limit: int = Query(default=10, ge=1, le=50),
    min_score: int = Query(default=0, ge=0, le=100),
    remote_only: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    jobs = fetch_jobs(search)

    filtered_jobs = []

    for job in jobs:

        if job["match_score"] < min_score:
            continue

        if remote_only:
            location = job["location"].lower()

            if "remote" not in location:
                continue

        filtered_jobs.append(job)

    saved_count = save_jobs_to_db(db, filtered_jobs)

    return {
        "search": search,
        "count": len(filtered_jobs[:limit]),
        "saved_new_jobs": saved_count,
        "jobs": filtered_jobs[:limit],
    }

@router.get("/saved")
def get_saved_jobs(
    limit: int = Query(default=20, ge=1, le=100),
    min_score: int = Query(default=0, ge=0, le=100),
    db: Session = Depends(get_db),
):
    saved_jobs = (
        db.query(Job)
        .filter(Job.match_score >= min_score)
        .order_by(Job.match_score.desc())
        .limit(limit)
        .all()
    )

    return {
        "count": len(saved_jobs),
        "jobs": saved_jobs,
    }

@router.delete("/saved/{job_id}")
def delete_saved_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully",
        "job_id": job_id,
    }