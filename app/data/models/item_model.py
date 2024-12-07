from sqlalchemy import Column, UUID, String, ForeignKey
import uuid

from app.data.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True)
    description = Column(String, index=True, default="No description")
    user_id = Column(UUID, ForeignKey("users.id"))