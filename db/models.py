from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    notes = relationship('DbNote', back_populates='owner', cascade='all, delete') 

class DbNote(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(ForeignKey('user.id'))

    owner = relationship('DbUser', back_populates='notes')
    history = relationship('DbNoteHistory', back_populates='note', cascade='all, delete')

class DbNoteHistory(Base):
    __tablename__ = 'note_history'
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(ForeignKey('note.id'))
    title = Column(String)
    description = Column(String)
    changed_at = Column(DateTime, default=datetime.utcnow)

    note = relationship('DbNote', back_populates='history')