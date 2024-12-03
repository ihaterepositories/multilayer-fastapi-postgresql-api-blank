from fastapi import Depends, APIRouter, Query, Body
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.data.database import get_db
from app.data import schemas
from app.services.item_service import ItemService

item_router = APIRouter()

def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    return ItemService(db)

@item_router.post("/items", response_model=schemas.ItemRead)
def create_item(item: schemas.ItemCreate = Body(..., embed=True), service: ItemService = Depends(get_item_service)):
    return service.create_item(item)

@item_router.get("/items", response_model=List[schemas.ItemRead])
def read_items(skip: int = 0, limit: int = 10, service: ItemService = Depends(get_item_service)):
    return service.get_items(skip, limit)

@item_router.get("/items/{item_id}", response_model=schemas.ItemRead)
def read_item(item_id: UUID, service: ItemService = Depends(get_item_service)):
    return service.get_item(item_id)

@item_router.put("/items/{item_id}", response_model=schemas.ItemRead)
def update_item(item_id: UUID, item: schemas.ItemCreate = Body(..., embed=True), service: ItemService = Depends(get_item_service)):
    return service.update_item(item_id, item)

@item_router.delete("/items/{item_id}")
def delete_item(item_id: UUID, service: ItemService = Depends(get_item_service)):
    return service.delete_item(item_id)