from fastapi import FastAPI

from app.data.database import engine
from app.data import models
from app.routes import item_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(item_router.item_router)

