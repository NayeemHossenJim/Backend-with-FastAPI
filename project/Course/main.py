# Essential imports
import model
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, get_db
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

class CourseRequest(BaseModel):
    name: str
    description: str
    credits: int
    hours_per_week: int

model.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def root(db: db_dependency):
    return db.query(model.Course).all()

@app.post("/courses")
async def create_course(course: CourseRequest, db: db_dependency):
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