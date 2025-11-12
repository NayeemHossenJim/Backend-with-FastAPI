# Essential imports
import model
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

class CourseRequest(BaseModel):
    name: str
    description: str
    credits: int
    hours_per_week: int

model.Base.metadata.create_all(bind=engine)

#Securely manage database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def root(db: db_dependency):
    return db.query(model.Todos).all()

@app.post("/courses")
async def create_course(course: CourseRequest):
    if course:
        return {"message": "Course created successfully", "course": course}
    return HTTPException(status_code=400, detail="Invalid course data")