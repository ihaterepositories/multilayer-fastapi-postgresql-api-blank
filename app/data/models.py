from sqlalchemy import Column, UUID, String, ForeignKey
import uuid

from app.data.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True)
    description = Column(String, index=True, default="No description")

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, index=True)
    email = Column(String, index=True)
    items = Column(UUID, ForeignKey("items.id"))