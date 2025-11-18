from pydantic import BaseModel, EmailStr, Field, field_validator

# Pydantic model for task creation requests
class ToDoRequest(BaseModel):
    task: str
    description: str
    priority: int = Field(..., ge=1, le=5, description="Priority must be between 1 and 5")
    status: bool = False
    
# Pydantic model for user creation requests
class CreateUser(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name must be between 2 and 100 characters")
    username: str = Field(..., min_length=3, max_length=50, description="Username must be between 3 and 50 characters")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128, description="Password must be between 8 and 128 characters")
    role: str = "user"  
    
    @field_validator('username')
    def validate_username(cls, v):
        import re
        if not re.match("^[a-zA-Z0-9_]+$", v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v  