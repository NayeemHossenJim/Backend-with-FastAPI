# Essential imports
from fastapi import FastAPI
from routers import task, user, admin
from database import Base, engine

# Initialize FastAPI app
app = FastAPI()

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(task.router)
app.include_router(user.router)
app.include_router(admin.router)