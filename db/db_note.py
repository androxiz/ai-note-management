from sqlalchemy.orm.session import Session
from schemas import NoteBase
from db.models import DbNote, DbNoteHistory, DbUser
from fastapi import HTTPException

from services.gemini import summaraze_note

def create_note(db:Session, request:NoteBase, current_user:DbUser):
    new_note = DbNote(
        title = request.title,
        description=request.description,
        owner_id = current_user.id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def get_all(db:Session):
    return db.query(DbNote).all()

def get_one(db:Session, id:int, current_user:DbUser):
    note = db.query(DbNote).filter(DbNote.id==id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f'Note {id} not found')
    if note.owner != current_user:
        raise HTTPException(status_code=403, detail=f'Forbidden')
    return note

def get_note_history(db:Session, id:int, current_user:DbUser):
    note=db.query(DbNote).filter(DbNote.id==id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f'Note {id} not found')
    if note.owner != current_user:
        raise HTTPException(status_code=403, detail=f'Forbidden')
    if not note.history:
        raise HTTPException(status_code=404, detail=f'History is empty')
    return note.history

def get_note_summary(db:Session, id:int, current_user:DbUser):
    note = db.query(DbNote).filter(DbNote.id==id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f'Note {id} not found')
    if note.owner != current_user:
        raise HTTPException(status_code=403, detail=f'Forbidden')

    response = summaraze_note(note.description)
    return {
        'note_id': note.id,
        'title': note.title,
        'summary': response
    }




def update_note(db:Session, id:int, request:NoteBase, current_user:DbUser):
    note = db.query(DbNote).filter(DbNote.id==id)

    if not note.first():
        raise HTTPException(status_code=404, detail=f'Note {id} not found')
    if note.first().owner != current_user:
        raise HTTPException(status_code=403, detail=f'Forbidden')
    
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


def delete_note(db:Session, id:int, current_user:DbUser):
    note = db.query(DbNote).filter(DbNote.id==id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f'Note {id} not found')
    if note.owner != current_user:
        raise HTTPException(status_code=403, detail=f'Forbidden')
    
    db.delete(note)
    db.commit()
    return {
        'message': f'Note {id} has been deleted'
    }

