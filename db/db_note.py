from schemas import NoteBase
from db.models import DbNote, DbNoteHistory, DbUser
from fastapi import HTTPException

from services.gemini import summaraze_note

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def check_note(db: AsyncSession, id: int, current_user: DbUser):
    stmt = (
        select(DbNote)
        .options(
            selectinload(DbNote.owner),
            selectinload(DbNote.history)
        )
        .where(DbNote.id == id)
    )
    
    result = await db.execute(stmt)
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(status_code=404, detail=f'Note {id} not found')
    if note.owner != current_user:
        raise HTTPException(status_code=403, detail=f'Forbidden')

    return note


async def create_note(db:AsyncSession, request:NoteBase, current_user:DbUser):
    new_note = DbNote(
        title = request.title,
        description=request.description,
        owner_id = current_user.id
    )

    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note

async def get_all(db:AsyncSession):
    stmt = select(DbNote).order_by(DbNote.id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_one(db:AsyncSession, id:int, current_user:DbUser):
    note = await check_note(db, id, current_user)
    return note

async def get_note_history(db:AsyncSession, id:int, current_user:DbUser):
    note = await check_note(db, id, current_user)
    if not note.history:
        raise HTTPException(status_code=404, detail=f'History is empty')
    return note.history

async def get_note_summary(db:AsyncSession, id:int, current_user:DbUser):
    note = await check_note(db, id, current_user)

    response = summaraze_note(note.description)
    return {
        'note_id': note.id,
        'title': note.title,
        'summary': response
    }


async def update_note(db:AsyncSession, id:int, request:NoteBase, current_user:DbUser):
    note = await check_note(db, id, current_user)
    
    note_history = DbNoteHistory(
        note_id = note.id,
        title = note.title,
        description = note.description
    )

    db.add(note_history)
    await db.commit()
    await db.refresh(note_history)

    note.title = request.title
    note.description = request.description

    await db.commit()
    await db.refresh(note)

    return note


async def delete_note(db:AsyncSession, id:int, current_user:DbUser):
    note = await check_note(db, id, current_user)
    
    await db.delete(note)
    await db.commit()

    return {
        'message': f'Note {id} has been deleted'
    }

