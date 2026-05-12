from sqlalchemy import Column, Integer, String
from backend.app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    url = Column(String, unique=True, index=True)
    category = Column(String)
    match_score = Column(Integer)