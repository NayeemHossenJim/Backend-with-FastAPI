# Essential imports
import model, schema
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from . user import get_current_user
from fastapi import Depends, HTTPException, APIRouter

# Initialize APIRouter
router = APIRouter(
    prefix="/tasks"
)
db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[dict, Depends(get_current_user)]

# Root endpoint to fetch all tasks
@router.get("/")
async def root(db: db_dependency, current_user: current_user_dependency):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(model.ToDo).filter(model.ToDo.owner_id == current_user["id"]).all()

#Endpoint to check speicific task by id
@router.get("/{task_id}")
async def get_task(task_id: int, db: db_dependency, current_user: current_user_dependency):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    Todo = db.query(model.ToDo).filter(model.ToDo.id == task_id).filter(model.ToDo.owner_id == current_user["id"]).first()
    if not Todo:
        return HTTPException(status_code=404, detail="Task not found")
    return Todo

# Endpoint to create a new tasks
@router.post("/")
async def create_task(new_task: schema.ToDoRequest, db: db_dependency, current_user: current_user_dependency):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    new_task = model.ToDo(
        task=new_task.task,
        description=new_task.description,
        priority=new_task.priority,
        status=new_task.status,
        owner_id=current_user["id"]
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created successfully", "task": new_task}

# Endpoint to update an existing task
@router.put("/{task_id}")
async def update_task(task_id: int, updated_task: schema.ToDoRequest, db: db_dependency, current_user: current_user_dependency):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    Todo = db.query(model.ToDo).filter(model.ToDo.id == task_id).filter(model.ToDo.owner_id == current_user["id"]).first()
    if not Todo:
        raise HTTPException(status_code=404, detail="Task not found")
    Todo.task = updated_task.task
    Todo.description = updated_task.description
    Todo.priority = updated_task.priority
    Todo.status = updated_task.status
    Todo.owner_id = current_user["id"]
    db.commit()
    db.refresh(Todo)
    return {"message": "Task updated successfully", "task": Todo}

# Endpoint to delete a task
@router.delete("/{task_id}")
async def delete_task(task_id: int, db: db_dependency, current_user: current_user_dependency):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    Todo = db.query(model.ToDo).filter(model.ToDo.id == task_id).filter(model.ToDo.owner_id == current_user["id"]).first()
    if not Todo:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(Todo)
    db.commit()
    return {"message": "Task deleted successfully"}