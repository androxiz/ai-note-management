from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import EmailStr

class UserBase(BaseModel):
    username: str = Field(..., description='The name of user', min_length=3)
    email: EmailStr = Field(..., description='User email')
    password: str = Field(..., description='Password', min_length=5)

class UserList(BaseModel):
    username: str
    email: str


class NoteBase(BaseModel):
    title: str = Field(..., description='Note title', min_length=4, max_length=25)
    description: str = Field(..., description='Note Description', min_length=3, max_length=255)

class NoteList(BaseModel):
    title: str
    description: str
    owner_id: int


class NoteHistoryList(BaseModel):
    title: str
    description: str
    changed_at: datetime