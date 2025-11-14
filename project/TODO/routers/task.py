# Essential imports
import model, schema
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

# Initialize APIRouter
router = APIRouter(
    prefix="/tasks"
)
db_dependency = Annotated[Session, Depends(get_db)]

# Root endpoint to fetch all tasks
@router.get("/")
async def root(db: db_dependency):
    return db.query(model.ToDo).all()

#Endpoint to check speicific task by id
@router.get("/{task_id}")
async def get_task(task_id: int, db: db_dependency):
    Todo = db.query(model.ToDo).filter(model.ToDo.id == task_id).first()
    if Todo:
        return Todo
    return HTTPException(status_code=404, detail="Task not found")

# Endpoint to create a new tasks
@router.post("/")
async def create_task(task: schema.ToDoRequest, db: db_dependency):
    new_task = model.ToDo(
        task=task.task,
        description=task.description,
        priority=task.priority,
        status=task.status,
        owner_id=task.owner_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created successfully", "task": new_task}

# Endpoint to update an existing task
@router.put("/{task_id}")
async def update_task(task_id: int, updated_task: schema.ToDoRequest, db: db_dependency):
    Todo = db.query(model.ToDo).filter(model.ToDo.id == task_id).first()
    if not Todo:
        raise HTTPException(status_code=404, detail="Task not found")
    Todo.task = updated_task.task
    Todo.description = updated_task.description
    Todo.priority = updated_task.priority
    Todo.status = updated_task.status
    Todo.owner_id = updated_task.owner_id
    db.commit()
    db.refresh(Todo)
    return {"message": "Task updated successfully", "task": Todo}

# Endpoint to delete a task
@router.delete("/{task_id}")
async def delete_task(task_id: int, db: db_dependency):
    Todo = db.query(model.ToDo).filter(model.ToDo.id == task_id).first()
    if not Todo:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(Todo)
    db.commit()
    return {"message": "Task deleted successfully"}