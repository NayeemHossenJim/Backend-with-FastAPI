from sqlalchemy import Column, Integer, String
from . database import Base

class userdata(Base):
    __tablename__ = "userdata"
    id = Column(Integer, primary_key = True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    age = Column(Integer, nullable= False)
    location = Column(String, nullable = False)