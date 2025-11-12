# Essential imports
from database import Base
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String

# SQLAlchemy model for tasks
class ToDo(Base):
    __tablename__ = "Todo"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(Integer, nullable=False)
    status = Column(Boolean, default=False)

# Pydantic model for task creation requests
class ToDoRequest(BaseModel):
    task: str
    description: str
    priority: int
    status: bool = False