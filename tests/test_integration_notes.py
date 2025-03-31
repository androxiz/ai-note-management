import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from main import app
from db.database import Base, get_db
from db.models import DbUser, DbNote
from schemas import NoteBase, NoteList
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

    test_user = DbUser(username="testuser", email="test@example.com", password="password")
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    test_note = DbNote(title="Test Note", description="This is a test note", owner_id=test_user.id)
    db.add(test_note)
    db.commit()
    db.refresh(test_note)

    test_note2 = DbNote(title="Test Note2", description="This is a test note2", owner_id=2)
    db.add(test_note2)
    db.commit()
    db.refresh(test_note2)

    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def auth_token():
    return create_access_token({"sub": "1"})

@pytest.fixture()
def headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

def test_create_note(headers):
    response = client.post("/note/create", json={
        "title": "New Note",
        "description": "New note description"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New Note"
    assert response.json()["description"] == "New note description"

def test_get_all_notes(headers):
    response = client.get("/note/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_one_note(headers):
    response = client.get("/note/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Note"

def test_update_note(headers):
    response = client.put("/note/1/update", json={
        "title": "Updated Note Title",
        "description": "Updated Description"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Note Title"
    assert response.json()["description"] == "Updated Description"

def test_delete_note(headers):
    response = client.delete("/note/1/delete", headers=headers)
    assert response.status_code == 200
    assert "has been deleted" in response.json()["message"]

def test_delete_foreign_note(headers):
    response = client.delete("/note/2/delete", headers=headers)
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

def test_get_note_summary(headers):
    response = client.get("/note/1/summarize", headers=headers)
    assert response.status_code == 200
    assert "summary" in response.json()

def test_get_note_history(headers):
    response = client.post("/note/create", json={
        "title": "Test Note",
        "description": "This is a test note"
    }, headers=headers)
    assert response.status_code == 200
    
    response = client.put(f"/note/{1}/update", json={
        "title": "Updated Test Note",
        "description": "This is an updated test note"
    }, headers=headers)
    assert response.status_code == 200
    
    response = client.get(f"/note/{1}/history", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_note_history_empty(headers):
    response = client.post("/note/create", json={
        "title": "Test Note",
        "description": "This note"
    }, headers=headers)
    assert response.status_code == 200

    response = client.get(f"/note/{1}/history", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "History is empty"}
