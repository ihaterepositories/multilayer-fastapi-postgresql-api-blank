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

    def get_all(self, sort: str = None, order: int = 1, skip: int = 0, limit: int = 0) -> List[T]:
        
        if limit > 0:
            if sort is None:
                entities = self.db.query(self.model).offset(skip).limit(limit).all()
            else:
                if order == 1:
                    entities = self.db.query(self.model).order_by(sort).offset(skip).limit(limit).all()
                else:
                    entities = self.db.query(self.model).order_by(sort.desc()).offset(skip).limit(limit).all()
        else:
            if sort is None:
                entities = self.db.query(self.model).offset(skip).all()
            else:
                if order == 1:
                    entities = self.db.query(self.model).order_by(sort).offset(skip).all()
                else:
                    entities = self.db.query(self.model).order_by(sort.desc()).offset(skip).all()

        return entities

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