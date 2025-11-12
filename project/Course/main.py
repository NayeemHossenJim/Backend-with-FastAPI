# Essential imports
import model
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine, get_db
from fastapi import Depends, FastAPI

# Initialize FastAPI app
app = FastAPI()

# Create database tables with dependencies
model.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

# Root endpoint to fetch all courses
@app.get("/")
async def root(db: db_dependency):
    return db.query(model.Course).all()

# Endpoint to create a new course
@app.post("/create_courses")
async def create_course(course: model.CourseRequest, db: db_dependency):
    new_course = model.Course(
        name=course.name,
        description=course.description,
        credits=course.credits,
        hours_per_week=course.hours_per_week
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"message": "Course created successfully", "course": new_course}