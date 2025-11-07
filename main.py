import time
import psycopg2
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor

app = FastAPI()

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

# Database Connection with Retry Logic
while True:
    try :
        connect = psycopg2.connect(host="localhost",database="postgres",user="postgres",password="1892",cursor_factory=RealDictCursor)
        cursor = connect.cursor()
        print("Database connection was successful!")
        break 
    except Exception as e:
        print("Database connection failed!")
        print("Error:", e)
        time.sleep(2)

@app.get("/")
async def db_test():
    cursor.execute("SELECT * FROM \"User\"")
    Data = cursor.fetchall()
    return {"Data": Data}