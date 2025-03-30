from db.models import DbUser
from schemas import UserBase
from hash import Hash
from sqlalchemy.orm.session import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.hash(request.password)
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='User with this credentials already exist')

    return new_user

def get_all(db:Session):
    return db.query(DbUser).all()


def get_one(db:Session, id:int):
    user = db.query(DbUser).filter(DbUser.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f'User {id} not found')
    return user

def update_user(db:Session, id:int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id==id)
    
    if not user.first():
         raise HTTPException(status_code=404, detail=f'User {id} not found')

    try:
        user.update({
            DbUser.username: request.username,
            DbUser.email: request.email,
            DbUser.password: Hash.hash(request.password)
        })

        db.commit()
        db.refresh(user.first())
    except IntegrityError:
        raise HTTPException(status_code=400, detail='User with this credentials already exist')
    
    return user.first()

def delete_user(db:Session, id:int):
    user = db.query(DbUser).filter(DbUser.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f'User {id} not found')
    db.delete(user)
    db.commit()
    return {
        'message': f'User {id} has been deleted successfully'
    }