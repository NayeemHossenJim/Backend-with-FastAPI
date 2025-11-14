# Essential imports
from fastapi import FastAPI
from database import Base, engine
from routers import task, user

# Initialize FastAPI app
app = FastAPI()

Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(task.router)
app.include_router(user.router)