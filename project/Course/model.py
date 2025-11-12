# Essential imports
from database import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

# SQLAlchemy model for Course
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    credits = Column(Integer)
    hours_per_week = Column(Integer)

# Pydantic model for course creation requests
class CourseRequest(BaseModel):
    name: str
    description: str
    credits: int
    hours_per_week: int