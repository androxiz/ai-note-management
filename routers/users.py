from fastapi import APIRouter, Depends, Path
from db import db_user
from sqlalchemy.orm.session import Session
from schemas import UserBase, UserList
from typing import List
from db.database import get_db

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/new', response_model=UserList)
def create_user(request: UserBase, db:Session = Depends(get_db)):
    return db_user.create_user(request=request, db=db)

@router.get('/', response_model=List[UserList])
def get_all(db: Session = Depends(get_db)):
    return db_user.get_all(db=db)

@router.get('/{id}', response_model=UserList)
def get_one(id:int = Path(..., description='User id to search for'), db:Session = Depends(get_db)):
    return db_user.get_one(db=db, id=id)

@router.put('/{id}/update', response_model=UserList)
def update_user(id:int, request:UserBase, db:Session = Depends(get_db)):
    return db_user.update_user(id=id, request=request, db=db)

@router.delete('/{id}/delete')
def delete_user(id:int, db:Session = Depends(get_db)):
    return db_user.delete_user(id=id, db=db)