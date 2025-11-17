import pytest
from main import app
from model import ToDo, User
from database import Base
from fastapi import status
from sqlalchemy import create_engine, event
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from routers.user import get_current_user, get_db
from datetime import datetime

# Use isolated in-memory SQLite for tests to avoid cross-run pollution
SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Provide a SQLite-compatible NOW() for server_default in models
@event.listens_for(engine, "connect")
def set_sqlite_now(dbapi_connection, connection_record):
    try:
        dbapi_connection.create_function(
            "now",
            0,
            lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        )
    except Exception:
        pass

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"id": 1, "username": "testuser", "role": "admin"}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def tasks():
    # Reset schema per test to ensure clean IDs and uniqueness
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    user = User(
        full_name="Test User",
        username="test_user",
        email="test@example.com",
        password="hashed_password",
        role="user",
        phone_number="1234567890",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    todo = ToDo(
        task="Test Todo",
        description="This is a test todo",
        priority=5,
        status=False,
        owner_id=user.id
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo


def test_read_all_authenticated(tasks):
    response = client.get("/tasks")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False,'task':'Test Todo',"id": 1, 'description': 'This is a test todo', "owner_id" : 1, "priority": 5}

def test_read_todo_by_id(tasks):
    response = client.get("/tasks/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False,'task':'Test Todo',"id": 1, 'description': 'This is a test todo', "owner_id" : 1, "priority": 5}

