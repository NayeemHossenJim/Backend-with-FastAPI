# Essential imports
from database import Base
from sqlalchemy import Boolean, Column, Integer, String

# SQLAlchemy model for tasks
class ToDo(Base):
    __tablename__ = "Todo"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(Integer, nullable=False)
    status = Column(Boolean, default=False)

