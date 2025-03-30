from fastapi import FastAPI
from routers import users, notes
from db import models
from db.database import engine

app = FastAPI()

app.include_router(users.router)
app.include_router(notes.router)

models.Base.metadata.create_all(engine)