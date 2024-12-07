from sqlalchemy import Column, UUID, String
import uuid

from app.data.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, index=True)
    email = Column(String, index=True)