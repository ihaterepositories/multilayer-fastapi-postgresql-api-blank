from typing import Type, TypeVar, Generic, List
from uuid import UUID

from sqlalchemy.orm import Session

T = TypeVar('T')

class GenericRepository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def create(self, entity: T) -> T:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get(self, id: UUID) -> T:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 10) -> List[T]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def update(self, updated_entity: T) -> T:
        self.db.commit()
        self.db.refresh(updated_entity)
        return updated_entity

    def delete(self, id: UUID) -> None:
        obj = self.db.query(self.model).filter(self.model.id == id).first()
        self.db.delete(obj)
        self.db.commit()