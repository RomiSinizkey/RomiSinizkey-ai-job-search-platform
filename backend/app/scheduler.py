from apscheduler.schedulers.background import BackgroundScheduler

from backend.app.services.job_scraper import fetch_jobs
from backend.app.services.notifications import send_new_jobs_notification


scheduler = BackgroundScheduler()


def scheduled_job_search():
    jobs = fetch_jobs("python")

    high_match_jobs = [
        job for job in jobs
        if job["match_score"] > 0
    ]

    if high_match_jobs:
        send_new_jobs_notification(high_match_jobs)

    print(f"Found {len(jobs)} jobs")


def start_scheduler():
    scheduler.add_job(
        scheduled_job_search,
        "interval",
        seconds=10
    )

    scheduler.start()

    print("Scheduler started")