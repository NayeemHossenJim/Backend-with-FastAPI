from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Basic Root Endpoint
@app.get("/")
async def root():
    return {"Message": "Hell Yeah!"}

# Path Parameter Example
@app.get("/path/{name}")
async def greet(name: str) -> dict:
    return {"Message": f"How are you {name}?"}

# Query Parameter Example
@app.get("/query")
async def scolding(name: str) -> dict:
    return {"Message": f"Get the Hell out of here {name}?"}

# Combining Path and Query Parameters
@app.get("/mix/{name}")
async def greet(name: str, age: int) -> dict:
    return {"Message": f"How are you {name}? ", "Age": f"You are {age} years old."}

# Optional Query Parameters
@app.get("/optional/{name}")
async def greet(name: Optional[str] = "Nayeem", age: int = 0) -> dict:
    if name and age:
        return {"Message": f"How are you {name}? ", "Age": f"You are {age} years old."}
    else:
        return {"Message": f"How are you {name}?"}
    
# User Model 
class User(BaseModel):
    Name: str
    Age: int
    City: str

# POST Request Handling
@app.post("/user")
async def create_user(user: User) -> dict:
    return {"User Data": user}