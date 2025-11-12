## Essential imports
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")

# Set up the database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Securely manage database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()