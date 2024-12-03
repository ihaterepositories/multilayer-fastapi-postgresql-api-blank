from sqlalchemy.orm import Session
from uuid import UUID

from app.data.schemas import ItemCreate
from app.data.models import Item
from app.repositories.item_repository import ItemRepository

class ItemService:
    def __init__(self, db: Session):
        self.repository = ItemRepository(db)

    def create_item(self, item: ItemCreate) -> Item:
        return self.repository.create(Item(**item.model_dump()))

    def get_items(self, skip: int = 0, limit: int = 10) -> list[Item]:
        return self.repository.get_all(skip, limit)
    
    def get_item(self, id: UUID) -> Item:
        return self.repository.get(id)
    
    def update_item(self, id: UUID, item: ItemCreate) -> Item:
        item_db = self.repository.get(id)
        if item_db is None:
            return None
        # Update the attributes of the existing item
        for key, value in item.model_dump().items():
            setattr(item_db, key, value)
        return self.repository.update(item_db)
    
    def delete_item(self, id: UUID) -> None:
        self.repository.delete(id)
    