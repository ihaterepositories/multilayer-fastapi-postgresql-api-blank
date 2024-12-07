from sqlalchemy.orm import Session
from typing import List

from app.data.models import Item
from app.repositories.interfaces.generic_repository import GenericRepository

class ItemRepository(GenericRepository[Item]):
    def __init__(self, db: Session):
        super().__init__(Item, db)

# Get item by user ID
    def get_by_user_id(self, user_id: str) -> List[Item]:
        return self.db.query(Item).filter(Item.user_id == user_id).all()