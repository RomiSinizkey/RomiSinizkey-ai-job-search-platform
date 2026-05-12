from sqlalchemy.orm import Session
from backend.app.models.job import Job


def save_jobs_to_db(db: Session, jobs: list[dict]) -> int:
    saved_count = 0

    for job_data in jobs:
        existing_job = db.query(Job).filter(Job.url == job_data["url"]).first()

        if existing_job:
            continue

        job = Job(
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            url=job_data["url"],
            category=job_data["category"],
            match_score=job_data["match_score"],
        )

        db.add(job)
        saved_count += 1

    db.commit()
    return saved_count