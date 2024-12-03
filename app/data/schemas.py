from pydantic import BaseModel
from typing import List
from uuid import UUID

class ItemRead(BaseModel):
    id: UUID
    name: str
    description: str

class ItemCreate(BaseModel):
    name: str
    description: str

class UserBase(BaseModel):
    username: str
    email: str
    items: List[ItemRead]