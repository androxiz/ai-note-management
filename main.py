from fastapi import FastAPI
from routers import users, notes, analytics
from db import models
from db.database import engine
from auth import authentication

app = FastAPI()

app.include_router(users.router)
app.include_router(notes.router)
app.include_router(analytics.router)
app.include_router(authentication.router)

models.Base.metadata.create_all(engine)