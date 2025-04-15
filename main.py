from fastapi import FastAPI
from routers import users, notes, analytics
from auth import authentication
import asyncio
from db.database import Base, engine
from sqlalchemy.ext.asyncio import AsyncEngine

app = FastAPI()

app.include_router(users.router)
app.include_router(notes.router)
app.include_router(analytics.router)
app.include_router(authentication.router)


async def init_models(engine:AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_models(engine))