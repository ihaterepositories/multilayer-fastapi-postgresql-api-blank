from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import redis.asyncio as redis
import json

from app.data.schemas.item_schemas import ItemCreate, ItemRead
from app.data.models.item_model import Item
from app.repositories.item_repository import ItemRepository
from app.utils.responding.models.base_response import BaseResponse
from app.utils.responding.response_creator import create_ok, create_error
from config import REDIS_HOST, REDIS_PORT

class ItemService:
    def __init__(self, db: AsyncSession):
        self.repository = ItemRepository(db)
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Get all items (sorting, ordering, skipping, and limiting supported)
    async def get_items(self, sort: str = None, order: int = 1, skip: int = 0, limit: int = 0) -> BaseResponse:

        try:
            items_orm = await self.repository.get_all(sort, order, skip, limit)

            if items_orm is None:
                return create_error("No items found")
            
            items_read = [ItemRead.model_validate(item_orm) for item_orm in items_orm]
            return create_ok("Items retrieved successfully", items_read)
        
        except Exception as e:
            return create_error(f"Error retrieving items: {e}", 500)

# Get a single item by ID
    async def get_item(self, id: UUID) -> BaseResponse:

        if id is None:
            return create_error("Item ID is required")
        
        if not self.repository.is_object_exists(id):
            return create_error(f"Item with the {id} ID does not exist")
        
        cache_key = f"item_{id}"
        cached_item_read = await self.redis_client.get(cache_key)

        if cached_item_read:
            return create_ok("Item found in cache", json.loads(cached_item_read))
        
        try:
            item_orm = await self.repository.get(id)

            if item_orm is None:
                return create_error("Item not found")
            
            item_read = ItemRead.model_validate(item_orm)
            await self.redis_client.set(cache_key, json.dumps(item_read.model_dump(), default=str), ex=3600)
            return create_ok("Item retrieved successfully", item_read)
        
        except Exception as e:
            return create_error(f"Error retrieving item: {e}", 500)
    
# Create a new item
    async def create_item(self, item_create: ItemCreate) -> BaseResponse:

        if item_create is None:
            return create_error("Item data is required")
        
        try:
            item_orm = await self.repository.create(Item(**item_create.model_dump()))
            return create_ok("Item created successfully", ItemRead.model_validate(item_orm))
        
        except Exception as e:
            return create_error(f"Error creating item: {e}", 500)

# Update an existing item
    async def update_item(self, id: UUID, item_create: ItemCreate) -> BaseResponse:
        
        if id is None:
            return create_error("Item ID is required")
    
        if item_create is None:
            return create_error("New item data is required")
        
        if not self.repository.is_object_exists(id):
            return create_error(f"Item with the {id} ID does not exist")
        
        try:
            item_orm = await self.repository.get(id)

            if item_orm is None:
                return create_error("Item not found")
            
            for key, value in item_create.model_dump().items():
                setattr(item_orm, key, value)

            item_updated = self.repository.update(item_orm)
            return create_ok("Item updated successfully", ItemRead.model_validate(item_updated))
        
        except Exception as e:
            return create_error(f"Error updating item: {e}", 500)
        
# Delete an item by ID
    async def delete_item(self, id: UUID) -> BaseResponse:

        if id is None:
            return create_error("Item ID is required")
        
        if not self.repository.is_object_exists(id):
            return create_error(f"Item with the {id} ID does not exist")
        
        try:
            await self.repository.delete(id)
            return create_ok("Item deleted successfully")
        
        except Exception as e:
            return create_error(f"Error deleting item: {e}", 500)
    