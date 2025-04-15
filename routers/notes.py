from fastapi import APIRouter, Depends
from schemas import NoteBase, NoteList, NoteHistoryList
from db import db_note
from db.database import get_db
from typing import List
from db.models import DbUser
from auth.oauth2 import get_current_user, oauth2_scheme

from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter(
    tags=['notes'],
    prefix='/note'
)

@router.post('/create', response_model=NoteList)
async def create_note(request:NoteBase, db:AsyncSession = Depends(get_db), current_user:DbUser=Depends(get_current_user)):
    return await db_note.create_note(db=db, request=request, current_user=current_user)

@router.get('/', response_model=List[NoteList])
async def get_all(db:AsyncSession=Depends(get_db), token:str=Depends(oauth2_scheme)):
    return await db_note.get_all(db=db)

@router.get('/{id}', response_model=NoteList)
async def get_one(id:int, db:AsyncSession=Depends(get_db), current_user:DbUser=Depends(get_current_user)):
    return await db_note.get_one(db=db, id=id, current_user=current_user)

@router.get('/{id}/history', response_model=List[NoteHistoryList])
async def get_note_history(id:int, db:AsyncSession=Depends(get_db), current_user:DbUser=Depends(get_current_user)):
    return await db_note.get_note_history(db=db, id=id, current_user=current_user)

@router.get('/{id}/summarize')
async def get_note_summary(id:int, db:AsyncSession=Depends(get_db), current_user:DbUser=Depends(get_current_user)):
    return await db_note.get_note_summary(db=db, id=id, current_user=current_user)

@router.put('/{id}/update', response_model=NoteList)
async def update_note(request:NoteBase, id:int, db:AsyncSession=Depends(get_db), current_user:DbUser=Depends(get_current_user)):
    return await db_note.update_note(db=db, id=id, request=request, current_user=current_user)

@router.delete('/{id}/delete')
async def delete_note(id:int, db:AsyncSession=Depends(get_db), current_user:DbUser=Depends(get_current_user)):
    return await db_note.delete_note(db=db, id=id, current_user=current_user)



