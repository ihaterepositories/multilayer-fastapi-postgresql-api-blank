from sqlalchemy.orm import Session

from app.data.models import User
from app.repositories.interfaces.generic_repository import GenericRepository

class UserRepository(GenericRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)