from fastapi import FastAPI

from backend.app.routes.jobs import router as jobs_router
from backend.app.database import engine, Base
from backend.app.models.job import Job
from backend.app.scheduler import start_scheduler

app = FastAPI(title="AI Job Search Platform")

Base.metadata.create_all(bind=engine)

app.include_router(jobs_router)

start_scheduler()

@app.get("/")
def root():
    return {"message": "Server is running"}