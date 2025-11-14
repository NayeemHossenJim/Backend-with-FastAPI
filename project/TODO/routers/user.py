# Essential imports
import model, schema, utils
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Depends, HTTPException, APIRouter

# Initialize APIRouter
router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

# Endpoint to create a new user
@router.post("/create_user")
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