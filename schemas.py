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
    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    title: str = Field(..., description='Note title')
    description: str = Field(..., description='Note Description')
    owner_id: int

class NoteList(BaseModel):
    title: str
    description: str
    owner: UserList
    class Config:
        from_attributes = True


class NoteHistoryList(BaseModel):
    title: str
    description: str
    changed_at: datetime