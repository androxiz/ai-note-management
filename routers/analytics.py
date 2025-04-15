from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from services import analyze

router = APIRouter(
    tags=['analytics'],
    prefix='/analtics'
)


@router.get('/')
async def get_analytics(db:AsyncSession=Depends(get_db)):
    return await analyze.analyze_notes(db=db)