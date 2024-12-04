from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ItemRead(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = "No description"

    class Config:
        orm_mode = True
        from_attributes = True

class ItemCreate(BaseModel):
    name: str
    description: str

class UserBase(BaseModel):
    username: str
    email: str
    items: List[ItemRead]