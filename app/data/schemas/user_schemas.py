from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

from app.data.schemas.item_schemas import ItemRead

class UserRead(BaseModel):
    id: UUID
    username: str
    email: str
    items: Optional[List[ItemRead]] = []

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str