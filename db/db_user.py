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


def get_one(db:Session, id:int, current_user:DbUser):
    user = db.query(DbUser).filter(DbUser.id==id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f'User {id} not found')
    if user != current_user:
        raise HTTPException(status_code=403, detail=f'Forbidden')
    
    return user


def get_user_notes(db:Session, id:int, current_user:DbUser):
    user = db.query(DbUser).filter(DbUser.id==id).first()
    if user != current_user:
        raise HTTPException(status_code=403, detail=f'Forbidden')
    if not user.notes:
        raise HTTPException(status_code=404, detail='User doesnt have any notes')
    return user.notes
    


def update_user(db:Session, id:int, request: UserBase, current_user:DbUser):
    user = db.query(DbUser).filter(DbUser.id==id)
    
    if not user.first():
         raise HTTPException(status_code=404, detail=f'User {id} not found')
    if user.first() != current_user:
        raise HTTPException(status_code=403, detail=f'Forbidden')
    
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

def delete_user(db:Session, id:int, current_user:DbUser):
    user = db.query(DbUser).filter(DbUser.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f'User {id} not found')
    if user != current_user:
        raise HTTPException(status_code=403, detail=f'Forbidden')
    
    db.delete(user)
    db.commit()
    return {
        'message': f'User {id} has been deleted successfully'
    }


def get_user_by_name(db:Session, username:str):
    user = db.query(DbUser).filter(DbUser.username==username).first()
    if not user:
         raise HTTPException(status_code=404, detail=f'User {username} not found')
    return user