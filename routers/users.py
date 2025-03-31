from fastapi import APIRouter, Depends
from db import db_user
from sqlalchemy.orm.session import Session
from schemas import UserBase, UserList, NoteList
from typing import List
from db.database import get_db
from db.models import DbUser
from auth.oauth2 import get_current_user, oauth2_scheme

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/new', response_model=UserList)
def create_user(request: UserBase, db:Session = Depends(get_db)):
    return db_user.create_user(request=request, db=db)

@router.get('/', response_model=List[UserList])
def get_all(db: Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    return db_user.get_all(db=db)

@router.get('/{id}', response_model=UserList)
def get_one(id:int, db:Session = Depends(get_db), current_user:DbUser=Depends(get_current_user)):
    return db_user.get_one(db=db, id=id, current_user=current_user)

@router.get('/{id}/notes', response_model=List[NoteList])
def get_user_notes(id:int, db:Session=Depends(get_db), current_user:DbUser=Depends(get_current_user)):
    return db_user.get_user_notes(db=db, id=id, current_user=current_user)

@router.put('/{id}/update', response_model=UserList)
def update_user(id:int, request:UserBase, db:Session = Depends(get_db), current_user:DbUser=Depends(get_current_user)):
    return db_user.update_user(id=id, request=request, db=db, current_user=current_user)

@router.delete('/{id}/delete')
def delete_user(id:int, db:Session = Depends(get_db), current_user:DbUser=Depends(get_current_user)):
    return db_user.delete_user(id=id, db=db, current_user=current_user)