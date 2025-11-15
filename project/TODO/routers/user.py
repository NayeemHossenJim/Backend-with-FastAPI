# Essential imports
import os
import model, schema, utils
from database import get_db
from typing import Annotated
from jose import JWTError, jwt
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Initialize APIRouter
router = APIRouter(
    prefix="/users"
)
db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

# Function to authenticate user credentials
async def Authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(model.User).filter(model.User.username == username).first()
    if not user:
        return False
    if not utils.verify_password(password, user.password):
        return False
    return user

# Create access token for authenticated user
def create_access_token(username: str, user_id : int, expire_delta=timedelta):
    encode = {"sub": username, "id": user_id}
    expire = datetime.now(timezone.utc) + expire_delta
    encode.update({"exp": expire})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):  
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

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
    access_token_expires = timedelta(minutes=20)
    access_token = create_access_token(user.username, user.id, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}