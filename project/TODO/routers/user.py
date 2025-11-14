# Essential imports
import model, schema, utils
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

# Initialize APIRouter
router = APIRouter(
    prefix="/users"
)
db_dependency = Annotated[Session, Depends(get_db)]

# Function to authenticate user credentials
async def Authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(model.User).filter(model.User.username == username).first()
    if not user:
        return False
    if not utils.verify_password(password, user.password):
        return False
    return user

# Endpoint to create a new user
@router.post("/")
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

# Endpoint for user login (token generation placeholder)
@router.post("/token")
async def login_for_access_token(from_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = await Authenticate_user(from_data.username, from_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return {"message": "Login successful"}