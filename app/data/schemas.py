from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ItemRead(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = "No description"
    user_id: UUID

    class Config:
        from_attributes = True

class ItemCreate(BaseModel):
    name: str
    description: str
    user_id: UUID

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