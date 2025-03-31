from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    notes = relationship('DbNote', back_populates='owner', cascade='all, delete') 

class DbNote(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner_id = Column(ForeignKey('user.id'))

    owner = relationship('DbUser', back_populates='notes')
    history = relationship('DbNoteHistory', back_populates='note', cascade='all, delete')

class DbNoteHistory(Base):
    __tablename__ = 'note_history'
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(ForeignKey('note.id'))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    changed_at = Column(DateTime, default=datetime.now(timezone.utc))

    note = relationship('DbNote', back_populates='history')