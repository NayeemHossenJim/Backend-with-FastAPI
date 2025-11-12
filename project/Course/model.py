from database import Base
from sqlalchemy import Column, Integer, String

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    credits = Column(Integer)
    hours_per_week = Column(Integer)