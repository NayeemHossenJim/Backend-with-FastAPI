import time
import psycopg2
from typing import Optional
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status

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
    name: str
    age: int
    city: str

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
    cursor.execute("SELECT * FROM userdata")
    Data = cursor.fetchall()
    return {"Data": Data}

#Save data to database
@app.post("/create_user")
async def create_user(post: User):
    cursor.execute("""INSERT INTO userdata(name, age, city) VALUES (%s, %s, %s) RETURNING *""", (post.name, str(post.age), post.city))
    new_user = cursor.fetchone()
    connect.commit()
    return {"New User": new_user}

#Fetch single user
@app.get("/fetch_user/{id}")
async def fetch_user(id: int):
    cursor.execute("SELECT * FROM userdata WHERE id = %s", (str(id),))
    user = cursor.fetchone()
    if user:
        return {"User": user}
    return Response(status_code=status.HTTP_404_NOT_FOUND)

#Delete user
@app.delete("/delete_user/{id}")
async def delete_user(id: int):
    cursor.execute("DELETE FROM userdata WHERE id = %s RETURNING *", (str(id),))
    deleted_user = cursor.fetchone()
    connect.commit()
    if deleted_user:
        return {"Deleted User": deleted_user}
    return Response(status_code=status.HTTP_404_NOT_FOUND)

#Update user
@app.put("/update_user/{id}")
async def update_user(id: int, post: User):
    cursor.execute("""UPDATE userdata SET name = %s, age = %s, city = %s WHERE id = %s RETURNING *""", (post.name, str(post.age), post.city, str(id)))
    updated_user = cursor.fetchone()
    connect.commit()
    if updated_user:
        return {"Updated User": updated_user}
    return Response(status_code=status.HTTP_404_NOT_FOUND)