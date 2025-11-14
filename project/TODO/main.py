# Essential imports
import model, schema, utils
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
    Todo = db.query(model.ToDo).filter(model.ToDo.id == task_id).first()
    if Todo:
        return Todo
    return HTTPException(status_code=404, detail="Task not found")

# Endpoint to create a new tasks
@app.post("/create_task")
async def create_task(task: schema.ToDoRequest, db: db_dependency):
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

# Endpoint to update an existing task
@app.put("/update_task/{task_id}")
async def update_task(task_id: int, updated_task: schema.ToDoRequest, db: db_dependency):
    Todo = db.query(model.ToDo).filter(model.ToDo.id == task_id).first()
    if not Todo:
        raise HTTPException(status_code=404, detail="Task not found")
    Todo.task = updated_task.task
    Todo.description = updated_task.description
    Todo.priority = updated_task.priority
    Todo.status = updated_task.status
    db.commit()
    db.refresh(Todo)
    return {"message": "Task updated successfully", "task": Todo}

# Endpoint to delete a task
@app.delete("/delete_task/{task_id}")
async def delete_task(task_id: int, db: db_dependency):
    Todo = db.query(model.ToDo).filter(model.ToDo.id == task_id).first()
    if not Todo:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(Todo)
    db.commit()
    return {"message": "Task deleted successfully"}

# Endpoint to create a new user
@app.post("/create_user")
async def create_user(user: schema.CreateUser, db: db_dependency):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = model.User(
        full_name=user.full_name,
        username=user.username,
        email=user.email,
        password=user.password
    )
    if db.query(model.User).filter(model.User.username == user.username).first():
        raise HTTPException(status_code=401, detail="Username already exists")
    if db.query(model.User).filter(model.User.email == user.email).first():
        raise HTTPException(status_code=401, detail="Email already exists")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": new_user}