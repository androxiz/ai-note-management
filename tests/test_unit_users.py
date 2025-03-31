import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm.session import Session
from db.models import DbUser
from db import db_user
from schemas import UserBase
from fastapi import HTTPException

def test_create_user():
    db = MagicMock(spec=Session)
    request = UserBase(username='testuser', email='test@example.com', password='password')
    
    with patch("hash.Hash.hash", return_value="hashedpassword"):
        user = db_user.create_user(db, request)
    
    db.add.assert_called_once()
    db.commit.assert_called_once()
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'

def test_get_all_users():
    db = MagicMock(spec=Session)
    db.query.return_value.all.return_value = [DbUser(id=1, username='test', email='test@example.com')]
    users = db_user.get_all(db)
    assert len(users) == 1
    assert users[0].username == 'test'

def test_get_one_user_not_found():
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        db_user.get_one(db, 1, DbUser(id=2))
    
    assert exc_info.value.status_code == 404

def test_update_user():
    db = MagicMock(spec=Session)
    
    user_mock = MagicMock(spec=DbUser)
    user_mock.id = 1
    user_mock.username = "oldname"
    user_mock.email = "old@example.com"

    db.query.return_value.filter.return_value.first.return_value = user_mock

    request = UserBase(username="newname", email="new@example.com", password="newpass")

    with patch("hash.Hash.hash", return_value="hashednewpass"):
        user_mock.username = request.username
        user_mock.email = request.email
        user_mock.password = "hashednewpass"

        updated_user = db_user.update_user(db, 1, request, user_mock)

    db.commit.assert_called_once()
    
    assert updated_user.username == "newname"
    assert updated_user.email == "new@example.com"




def test_delete_user():
    db = MagicMock(spec=Session)
    user_mock = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = user_mock
    
    response = db_user.delete_user(db, 1, user_mock)
    
    db.delete.assert_called_once_with(user_mock)
    db.commit.assert_called_once()
    assert response["message"] == "User 1 has been deleted successfully"