from fastapi import FastAPI
import asyncio

from app.data.database import engine, Base
from app.routes.item_router import item_router
from app.routes.user_router import user_router

app = FastAPI()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await create_tables()

app.include_router(item_router)
app.include_router(user_router)