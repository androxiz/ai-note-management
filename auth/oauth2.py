from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError

from fastapi import Depends, HTTPException
from db.database import get_db
from sqlalchemy.orm.session import Session
 
from db import db_user

import os
from dotenv import load_dotenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 

if not SECRET_KEY:
    raise ValueError("SECRET_KEY Not found in the env file")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credential_exception = HTTPException(
       status_code=401,
       detail="Could not validate credentials",
       headers={'WWW-Authenticate': "Bearer"}
    )
    try:
       payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
       username: str = payload.get('sub')
       if username is None:
          raise credential_exception
    except JWTError:
       raise credential_exception
    
    user = db_user.get_user_by_name(db=db, username=username)

    if user is None:
       raise credential_exception
    
    return user