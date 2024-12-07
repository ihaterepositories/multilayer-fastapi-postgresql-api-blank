from typing import Type, TypeVar, Generic, List
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import desc

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

    def get_all(self, sort: str = None, order: int = 1, skip: int = 0, limit: int = 0) -> List[T]:
        
        query = self.db.query(self.model)
    
        if sort:
            column = getattr(self.model, sort)
            if order == 1:
                query = query.order_by(column)
            else:
                query = query.order_by(desc(column))
    
        query = query.offset(skip)
    
        if limit > 0:
            query = query.limit(limit)
    
        return query.all()

    def update(self, updated_entity: T) -> T:
        self.db.commit()
        self.db.refresh(updated_entity)
        return updated_entity

    def delete(self, id: UUID) -> None:
        obj = self.db.query(self.model).filter(self.model.id == id).first()
        self.db.delete(obj)
        self.db.commit()

    def is_object_exists(self, id: UUID) -> bool:
        return self.db.query(self.model).filter(self.model.id == id).first() is not None