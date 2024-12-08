from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import Type, TypeVar, Generic, List
from uuid import UUID

T = TypeVar('T')

class GenericRepository(Generic[T]):
    def __init__(self, model: Type[T], db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, entity: T) -> T:
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def get(self, id: UUID) -> T:
        result = await self.db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_all(self, sort: str = None, order: int = 1, skip: int = 0, limit: int = 0) -> List[T]:
        query = select(self.model)
        
        if sort:
            column = getattr(self.model, sort)
            if order == 1:
                query = query.order_by(column)
            else:
                query = query.order_by(desc(column))
        
        query = query.offset(skip)
        
        if limit > 0:
            query = query.limit(limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, updated_entity: T) -> T:
        await self.db.commit()
        await self.db.refresh(updated_entity)
        return updated_entity

    async def delete(self, id: UUID) -> None:
        result = await self.db.execute(select(self.model).filter(self.model.id == id))
        obj = result.scalars().first()
        await self.db.delete(obj)
        await self.db.commit()

    async def is_object_exists(self, id: UUID) -> bool:
        result = await self.db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first() is not None