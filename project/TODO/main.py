import model
from database import engine
from fastapi import FastAPI

app = FastAPI()

model.Base.metadata.create_all(bind=engine)