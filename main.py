# Essential imports
from fastapi import FastAPI, Request
from routers import task, user, admin
from fastapi.templating import Jinja2Templates
from database import Base, engine

# Initialize FastAPI app
app = FastAPI()

# Create database tables and templates directory
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(task.router)
app.include_router(user.router)
app.include_router(admin.router)