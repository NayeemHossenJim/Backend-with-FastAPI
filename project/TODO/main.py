import model
from model import Todos
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
from database import engine, SessionLocal

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def read_root(db: db_dependency):
    return db.query(Todos).all()