from apscheduler.schedulers.background import BackgroundScheduler

from backend.app.services.job_scraper import fetch_jobs


scheduler = BackgroundScheduler()


def scheduled_job_search():
    jobs = fetch_jobs("python")

    print(f"Found {len(jobs)} jobs")


def start_scheduler():
    scheduler.add_job(
        scheduled_job_search,
        "interval",
        minutes=1
    )

    scheduler.start()
    