# Essential imports
from database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text, ForeignKey

# SQLAlchemy model for tasks
class ToDo(Base):
    __tablename__ = "Todo"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(Integer, nullable=False)
    status = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("User.id"), nullable=False)

# SQLAlchemy model for users
class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    role = Column(String, nullable=False)
    phone_number = Column(String(length=11), nullable=True)  