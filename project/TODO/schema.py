from pydantic import BaseModel

# Pydantic model for task creation requests
class ToDoRequest(BaseModel):
    task: str
    description: str
    priority: int
    status: bool = False