from sqlalchemy.orm.session import Session
from schemas import NoteBase, NoteList
from db.models import DbNote, DbNoteHistory
from fastapi import HTTPException
from datetime import datetime

def create_note(db:Session, request:NoteBase):
    new_note = DbNote(
        title = request.title,
        description=request.description,
        owner_id = request.owner_id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def get_all(db:Session):
    return db.query(DbNote).all()

def get_one(db:Session, id:int):
    note = db.query(DbNote).filter(DbNote.id==id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f'Note {id} not found')
    return note

def get_note_history(db:Session, id:int):
    note=db.query(DbNote).filter(DbNote.id==id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f'Note {id} not found')
    return note.history

def update_note(db:Session, id:int, request:NoteBase):
    note = db.query(DbNote).filter(DbNote.id==id)
    
    if not note.first():
        raise HTTPException(status_code=404, detail=f'Note {id} not found')
    
    note_history = DbNoteHistory(
        note_id = note.first().id,
        title = note.first().title,
        description = note.first().description
    )

    db.add(note_history)
    db.commit()
    db.refresh(note_history)

    note.update({
        DbNote.title: request.title,
        DbNote.description: request.description
    })

    db.commit()
    db.refresh(note.first())
    return note.first()


def delete_note(db:Session, id:int):
    note = db.query(DbNote).filter(DbNote.id==id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f'Note {id} not found')
    
    db.delete(note)
    db.commit()
    return {
        'message': f'Note {id} has been deleted'
    }

