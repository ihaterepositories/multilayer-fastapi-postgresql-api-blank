from fastapi import Depends, APIRouter, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.data.database import get_db
from app.data.schemas.item_schemas import ItemCreate
from app.utils.responding.models.base_response import BaseResponse
from app.services.item_service import ItemService

item_router = APIRouter()

def get_item_service(db: AsyncSession = Depends(get_db)) -> ItemService:
    return ItemService(db)

@item_router.get("/items", response_model=BaseResponse)
async def read_items(
    sort: str = Query(None, description="Sort options (leave empty for no sorting) : name, description"), 
    order: int = Query(1, description="Sort order: 1 for ascending, -1 for descending"), 
    skip: int = Query(0, description="Skip some count of first items"), 
    limit: int = Query(0, description="Limit the number of items (0 - no limit)"), 
    service: ItemService = Depends(get_item_service)):
    return await service.get_items(sort, order, skip, limit)

@item_router.get("/item", response_model=BaseResponse)
async def read_item(
    item_id: UUID = Query(..., description="Item ID"),
    service: ItemService = Depends(get_item_service)):
    return await service.get_item(item_id)

@item_router.post("/items", response_model=BaseResponse)
async def create_item(
    item: ItemCreate = Body(..., embed=True), 
    service: ItemService = Depends(get_item_service)):
    return await service.create_item(item)

@item_router.put("/items", response_model=BaseResponse)
async def update_item(
    item_id: UUID = Query(..., description="Item ID"),
    item: ItemCreate = Body(..., embed=True), 
    service: ItemService = Depends(get_item_service)):
    return await service.update_item(item_id, item)

@item_router.delete("/items", response_model=BaseResponse)
async def delete_item(
    item_id: UUID = Query(..., description="Item ID"),
    service: ItemService = Depends(get_item_service)):
    return await service.delete_item(item_id)