from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select

from app.data.models.item_model import Item
from app.repositories.interfaces.generic_repository import GenericRepository

class ItemRepository(GenericRepository[Item]):
    def __init__(self, db: Session):
        super().__init__(Item, db)

# Get item by user ID
    async def get_by_user_id(self, user_id: str) -> List[Item]:
        result = await self.db.execute(select(Item).filter(Item.user_id == user_id))
        return result.scalars().all()