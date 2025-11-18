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

# Validate required environment variables
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")
if not ALGORITHM:
    raise ValueError("ALGORITHM environment variable is not set")

# Initialize APIRouter
router = APIRouter(
    prefix="/users",
    tags=["users"]
)
db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="users/token")

# Function to authenticate user credentials
async def Authenticate_user(username: str, password: str, db: db_dependency):
    try:
        user = db.query(model.User).filter(model.User.username == username).first()
        if not user:
            return False
        
        # Verify password
        if not utils.verify_password(password, user.password):
            return False
        
        return user
    except Exception as e:
        print(f"Authentication error: {e}")
        return False

# Create access token for authenticated user
def create_access_token(username: str, user_id: int, role: str, expire_delta: timedelta = None):
    if expire_delta is None:
        expire_delta = timedelta(minutes=20)
    
    encode = {"sub": username, "id": user_id, "role": role}
    expire = datetime.now(timezone.utc) + expire_delta
    encode.update({"exp": expire})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):  
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return {"username": username, "id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# Endpoint to create a new user
@router.post("/")
async def create_user(user: schema.CreateUser, db: db_dependency):
    # Validate password length before hashing
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    # Check if username already exists
    if db.query(model.User).filter(model.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email already exists
    if db.query(model.User).filter(model.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash password
    hashed_password = utils.hash_password(user.password)
    
    # Create new user with hashed password
    new_user = model.User(
        full_name=user.full_name,
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully", "user": {"id": new_user.id, "username": new_user.username, "email": new_user.email, "role": new_user.role}}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")

# Health check endpoint for user routes
@router.get("/health")
async def user_health_check():
    return {"status": "healthy", "service": "user authentication"}

# Get current user endpoint
@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

# Endpoint for user login (token generation)
@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = await Authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=20)
    access_token = create_access_token(
        username=user.username, 
        user_id=user.id, 
        role=user.role, 
        expire_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "expires_in": 1200  # 20 minutes in seconds
    }