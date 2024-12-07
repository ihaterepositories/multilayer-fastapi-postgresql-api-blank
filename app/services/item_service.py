from sqlalchemy.orm import Session
from uuid import UUID

from app.data.schemas import ItemCreate, ItemRead
from app.data.models import Item
from app.repositories.item_repository import ItemRepository
from app.utils.responding.models.base_response import BaseResponse
from app.utils.responding.response_creator import create_ok, create_error

class ItemService:
    def __init__(self, db: Session):
        self.repository = ItemRepository(db)

# Get all items (sorting, ordering, skipping, and limiting supported)
    def get_items(self, sort: str = None, order: int = 1, skip: int = 0, limit: int = 0) -> BaseResponse:
        
        try:
            items_orm = self.repository.get_all(sort, order, skip, limit)

            if items_orm is None:
                return create_error("No items found")
            
            items_read = [ItemRead.model_validate(item_orm) for item_orm in items_orm]
            return create_ok("Items retrieved successfully", items_read)
        
        except Exception as e:
            return create_error(f"Error retrieving items: {e}", 500)

# Get a single item by ID
    def get_item(self, id: UUID) -> BaseResponse:

        if id is None:
            return create_error("Item ID is required")
        
        if not self.repository.is_object_exists(id):
            return create_error(f"Item with the {id} ID does not exist")
        
        try:
            item_orm = self.repository.get(id)

            if item_orm is None:
                return create_error("Item not found")
            
            item_read = ItemRead.model_validate(item_orm)
            return create_ok("Item retrieved successfully", item_read)
        
        except Exception as e:
            return create_error(f"Error retrieving item: {e}", 500)
    
# Create a new item
    def create_item(self, item_create: ItemCreate) -> BaseResponse:

        if item_create is None:
            return create_error("Item data is required")
        
        try:
            item_orm = self.repository.create(Item(**item_create.model_dump()))
            return create_ok("Item created successfully", ItemRead.model_validate(item_orm))
        
        except Exception as e:
            return create_error(f"Error creating item: {e}", 500)

# Update an existing item
    def update_item(self, id: UUID, item_create: ItemCreate) -> BaseResponse:
        
        if id is None:
            return create_error("Item ID is required")
    
        if item_create is None:
            return create_error("New item data is required")
        
        if not self.repository.is_object_exists(id):
            return create_error(f"Item with the {id} ID does not exist")
        
        try:
            item_orm = self.repository.get(id)

            if item_orm is None:
                return create_error("Item not found")
            
            for key, value in item_create.model_dump().items():
                setattr(item_orm, key, value)

            item_updated = self.repository.update(item_orm)
            return create_ok("Item updated successfully", ItemRead.model_validate(item_updated))
        
        except Exception as e:
            return create_error(f"Error updating item: {e}", 500)
        
# Delete an item by ID
    def delete_item(self, id: UUID) -> BaseResponse:

        if id is None:
            return create_error("Item ID is required")
        
        if not self.repository.is_object_exists(id):
            return create_error(f"Item with the {id} ID does not exist")
        
        try:
            self.repository.delete(id)
            return create_ok("Item deleted successfully")
        
        except Exception as e:
            return create_error(f"Error deleting item: {e}", 500)
    