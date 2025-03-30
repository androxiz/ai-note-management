from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import EmailStr

class UserBase(BaseModel):
    username: str = Field(..., description='The name of user')
    email: EmailStr = Field(..., description='User email')
    password: str = Field(..., description='Password')

class UserList(BaseModel):
    username: str
    email: str


class NoteBase(BaseModel):
    title: str = Field(..., description='Note title')
    description: str = Field(..., description='Note Description')

class NoteList(BaseModel):
    title: str
    description: str
    owner_id: int


class NoteHistoryList(BaseModel):
    title: str
    description: str
    changed_at: datetime