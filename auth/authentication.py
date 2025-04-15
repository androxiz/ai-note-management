from fastapi import APIRouter

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from fastapi import Depends, HTTPException

from db.database import get_db

from db.models import DbUser

from hash import Hash
from auth import oauth2

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter(
    tags=['auth']
)

@router.post('/token')
async def get_token(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DbUser).where(DbUser.username == request.username))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail="Incorrect password")

    access_token = oauth2.create_access_token(data={'sub': str(user.id)})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }