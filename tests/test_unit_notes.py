import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm.session import Session
from db.models import DbNote, DbNoteHistory, DbUser
from db import db_note
from schemas import NoteBase
from fastapi import HTTPException

@pytest.fixture
def current_user():
    return DbUser(id=1, username="testuser", email="test@example.com")

@pytest.fixture
def note_mock(current_user):
    note = MagicMock(spec=DbNote)
    note.id = 1
    note.title = "Test Note"
    note.description = "Test Description"
    note.owner_id = current_user.id
    note.owner = current_user
    return note

def test_create_note(current_user):
    db = MagicMock(spec=Session)
    request = NoteBase(title="New Note", description="New Description")
    
    new_note = db_note.create_note(db, request, current_user)
    
    db.add.assert_called_once()
    db.commit.assert_called_once()
    assert new_note.title == "New Note"
    assert new_note.description == "New Description"
    assert new_note.owner_id == current_user.id

def test_get_all_notes():
    db = MagicMock(spec=Session)
    db.query.return_value.all.return_value = [
        DbNote(id=1, title="Note 1", description="Desc 1", owner_id=1)
    ]
    
    notes = db_note.get_all(db)
    
    assert len(notes) == 1
    assert notes[0].title == "Note 1"

def test_get_one_note(note_mock, current_user):
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = note_mock
    
    note = db_note.get_one(db, note_mock.id, current_user)
    
    assert note.id == note_mock.id
    assert note.title == "Test Note"

def test_get_note_history(note_mock, current_user):
    db = MagicMock(spec=Session)
    history_mock = MagicMock(spec=DbNoteHistory)
    note_mock.history = [history_mock]
    db.query.return_value.filter.return_value.first.return_value = note_mock
    
    history = db_note.get_note_history(db, note_mock.id, current_user)
    
    assert len(history) > 0

def test_get_note_history_empty(note_mock, current_user):
    db = MagicMock(spec=Session)
    note_mock.history = []
    db.query.return_value.filter.return_value.first.return_value = note_mock
    
    with pytest.raises(HTTPException) as exc_info:
        db_note.get_note_history(db, note_mock.id, current_user)
    
    assert exc_info.value.status_code == 404

def test_get_note_summary(note_mock, current_user):
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = note_mock

    with patch("db.db_note.summaraze_note", return_value="Summary Text") as mock_summarize:
        summary = db_note.get_note_summary(db, note_mock.id, current_user)

    mock_summarize.assert_called_once_with(note_mock.description)
    assert summary["note_id"] == note_mock.id
    assert summary["title"] == note_mock.title
    assert summary["summary"] == "Summary Text"

def test_update_note(note_mock, current_user):
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = note_mock
    
    request = NoteBase(title="Updated Title", description="Updated Description")
    
    note_mock.title = request.title
    note_mock.description = request.description

    updated_note = db_note.update_note(db, note_mock.id, request, current_user)
    
    
    assert updated_note.title == "Updated Title"
    assert updated_note.description == "Updated Description"



def test_delete_note(note_mock, current_user):
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = note_mock
    
    response = db_note.delete_note(db, note_mock.id, current_user)
    
    db.delete.assert_called_once_with(note_mock)
    db.commit.assert_called_once()
    assert response["message"] == f"Note {note_mock.id} has been deleted"
