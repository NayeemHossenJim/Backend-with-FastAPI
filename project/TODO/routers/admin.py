# Essential imports
import model, schema
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from . user import get_current_user
from fastapi import Depends, HTTPException, APIRouter

# Initialize APIRouter
router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)
db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[dict, Depends(get_current_user)]

# Root endpoint to fetch all tasks
@router.get("/tasks")
async def root(db: db_dependency, current_user: current_user_dependency):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(model.ToDo).all()

# Endpoint to fetch all users
@router.get("/users")
async def get_users(db: db_dependency, current_user: current_user_dependency):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(model.User).all()

# Endpoint to delete a task by id
@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: db_dependency, current_user: current_user_dependency):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    Todo = db.query(model.ToDo).filter(model.ToDo.id == task_id).first()
    if not Todo:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(Todo)
    db.commit()
    return {"message": "Task deleted successfully"}