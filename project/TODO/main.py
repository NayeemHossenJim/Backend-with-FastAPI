# Essential imports
import model
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine, get_db
from fastapi import Depends, FastAPI, HTTPException

# Initialize FastAPI app
app = FastAPI()

# Create database tables with dependencies
model.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

# Root endpoint to fetch all tasks
@app.get("/")
async def root(db: db_dependency):
    return db.query(model.ToDo).all()

#Endpoint to check speicific task by id
@app.get("/task/{task_id}")
async def get_task(task_id: int, db: db_dependency):
    task = db.query(model.ToDo).filter(model.ToDo.id == task_id).first()
    if task:
        return task
    return HTTPException(status_code=404, detail="Task not found")

# Endpoint to create a new tasks
@app.post("/create_task")
async def create_task(task: model.ToDoRequest, db: db_dependency):
    new_task = model.ToDo(
        task=task.task,
        description=task.description,
        priority=task.priority,
        status=task.status
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created successfully", "task": new_task}