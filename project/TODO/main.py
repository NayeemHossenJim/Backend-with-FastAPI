# Essential imports
from fastapi import FastAPI
from routers import task, user

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(task.router)
app.include_router(user.router)
