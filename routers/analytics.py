from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from services import analyze

router = APIRouter(
    tags=['analytics'],
    prefix='/analtics'
)


@router.get('/')
def get_analytics(db:Session=Depends(get_db)):
    return analyze.analyze_notes(db=db)