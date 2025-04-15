from db.models import DbUser
from schemas import UserBase
from hash import Hash
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def check_user(db: AsyncSession, id: int, current_user: DbUser):
    user = await db.get(DbUser, id)

    if not user:
        raise HTTPException(status_code=404, detail=f'User {id} not found')
    if user != current_user:
        raise HTTPException(status_code=403, detail=f'Forbidden')

    return user


async def create_user(db: AsyncSession, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.hash(request.password)
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='User with this credentials already exist')

    return new_user

async def get_all(db:AsyncSession):
    stmt = select(DbUser).order_by(DbUser.id)
    result = await db.execute(stmt)
    notes = result.scalars().all()
    return notes


async def get_one(db:AsyncSession, id:int, current_user:DbUser):
    user = await check_user(db, id, current_user)
    return user


async def get_user_notes(db:AsyncSession, id:int, current_user:DbUser):
    user = await check_user(db, id, current_user)
    if not user.notes:
        raise HTTPException(status_code=404, detail='User doesnt have any notes')
    return user.notes
    

async def update_user(db:AsyncSession, id:int, request: UserBase, current_user:DbUser):
    user = await check_user(db, id, current_user)

    try:
        user.username = request.username
        user.email = request.email
        user.password = Hash.hash(request.password)

        await db.commit()
        await db.refresh(user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='User with this credentials already exist')
    
    return user

async def delete_user(db:AsyncSession, id:int, current_user:DbUser):
    user = await check_user(db, id, current_user)
    await db.delete(user)
    await db.commit()
    return {
        'message': f'User {id} has been deleted successfully'
    }
