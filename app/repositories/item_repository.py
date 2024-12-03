from sqlalchemy.orm import Session
from app.data.models import Item
from app.repositories.interfaces.generic_repository import GenericRepository

class ItemRepository(GenericRepository[Item]):
    def __init__(self, db: Session):
        super().__init__(Item, db)

    