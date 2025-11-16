from pydantic import BaseModel, EmailStr, Field

# Pydantic model for task creation requests
class ToDoRequest(BaseModel):
    task: str
    description: str
    priority: int
    status: bool = False
    
# Pydantic model for user creation requests
class CreateUser(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128, description="Password must be greater than 8 characters")