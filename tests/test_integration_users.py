import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from fastapi.testclient import TestClient
from fastapi import HTTPException
from db.models import DbUser
from db import db_user
from schemas import UserBase
from main import app
from db.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hash import Hash
from auth.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    hashed_password = Hash.hash("password")
    test_user = DbUser(username="testuser", email="test@example.com", password=hashed_password)
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def auth_token():
    return create_access_token({"sub": "1"})

@pytest.fixture()
def headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

def test_create_user():
    response = client.post("/user/new", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "newpassword"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"

def test_get_all_users(headers):
    response = client.get("/user/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_one_user(headers):
    response = client.get("/user/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_update_user(headers):
    response = client.put("/user/1/update", json={
        "username": "updateduser",
        "email": "updated@example.com",
        "password": "newpassword"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"

def test_delete_user(headers):
    response = client.delete("/user/1/delete", headers=headers)
    assert response.status_code == 200
    assert "has been deleted" in response.json()["message"]


def test_create_duplicate_user():
    db = MagicMock(spec=Session)
    request = UserBase(username='testuser', email='test@example.com', password='password')

    db.commit.side_effect = IntegrityError("", "", "")

    with pytest.raises(HTTPException) as exc_info:
        db_user.create_user(db, request)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "User with this credentials already exist"

def test_delete_foreign_user():
    db = MagicMock(spec=Session)
    user_mock = MagicMock()
    user_mock.id = 2
    
    db.query.return_value.filter.return_value.first.return_value = MagicMock(id=1)
    
    with pytest.raises(HTTPException) as exc_info:
        db_user.delete_user(db, 1, user_mock)
    
    assert exc_info.value.status_code == 403
    assert "Forbidden" in exc_info.value.detail

def test_token_invalid_password():
    response = client.post("/token", data={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 404
    assert "Incorrect password" in response.json()["detail"]

def test_token_nonexistent_user():
    response = client.post("/token", data={"username": "nouser", "password": "password"})
    assert response.status_code == 404
    assert "Invalid credentials" in response.json()["detail"]