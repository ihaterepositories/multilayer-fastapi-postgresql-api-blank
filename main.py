from fastapi import FastAPI

from app.data.database import engine, Base
from app.routes import item_router, user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(item_router.item_router)
app.include_router(user_router.user_router)