from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from schemas import NoteBase, NoteList, NoteHistoryList
from db import db_note
from db.database import get_db
from typing import List

router = APIRouter(
    tags=['notes'],
    prefix='/note'
)

@router.post('/create', response_model=NoteList)
def create_note(request:NoteBase, db:Session = Depends(get_db)):
    return db_note.create_note(db=db, request=request)

@router.get('/', response_model=List[NoteList])
def get_all(db:Session=Depends(get_db)):
    return db_note.get_all(db=db)

@router.get('/{id}', response_model=NoteList)
def get_one(id:int, db:Session=Depends(get_db)):
    return db_note.get_one(db=db, id=id)

@router.get('{id}/history', response_model=List[NoteHistoryList])
def get_note_history(id:int, db:Session=Depends(get_db)):
    return db_note.get_note_history(db=db, id=id)

@router.put('/{id}/update', response_model=NoteList)
def update_note(request:NoteBase, id:int, db:Session=Depends(get_db)):
    return db_note.update_note(db=db, id=id, request=request)

@router.delete('{id}/delete')
def delete_note(id:int, db:Session=Depends(get_db)):
    return db_note.delete_note(db=db, id=id)



