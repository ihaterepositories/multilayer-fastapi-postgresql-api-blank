from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import redis.asyncio as redis
import json

from app.data.schemas.user_schemas import UserCreate, UserRead
from app.data.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.repositories.item_repository import ItemRepository
from app.utils.responding.models.base_response import BaseResponse
from app.utils.responding.response_creator import create_ok, create_error
from config import REDIS_HOST, REDIS_PORT

class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
        self.item_repository = ItemRepository(db)
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Get all users (sorting, ordering, skipping, and limiting supported)
    async def get_users(self, sort: str = None, order: int = 1, skip: int = 0, limit: int = 0) -> BaseResponse:

        try:
            users_orm = await self.repository.get_all(sort, order, skip, limit)

            for user in users_orm:
                user.items = await self.item_repository.get_by_user_id(user.id)

            if users_orm is None:
                return create_error("No users found")
            
            users_read = [UserRead.model_validate(user_orm) for user_orm in users_orm]
            return create_ok("Users retrieved successfully", users_read)
        
        except Exception as e:
            return create_error(f"Error retrieving users: {e}", 500)
        
# Get a single user by ID
    async def get_user(self, id: UUID) -> BaseResponse:

        if id is None:
            return create_error("User ID is required")
        
        if not self.repository.is_object_exists(id):
            return create_error(f"User with the {id} ID does not exist")
        
        cache_key = f"user_{id}"
        cached_user_read = await self.redis_client.get(cache_key)

        if cached_user_read:
            return create_ok("User found in cache", json.loads(cached_user_read))
        
        try:
            user_orm = await self.repository.get(id)
            user_orm.items = await self.item_repository.get_by_user_id(user_orm.id)

            if user_orm is None:
                return create_error("User not found")
            
            user_read = UserRead.model_validate(user_orm)
            await self.redis_client.set(cache_key, json.dumps(user_read.model_dump(), default=str), ex=3600)
            return create_ok("User retrieved successfully", user_read)
        
        except Exception as e:
            return create_error(f"Error retrieving user: {e}", 500)
        
# Create a new user
    async def create_user(self, user_create: UserCreate) -> BaseResponse:

        if user_create is None:
            return create_error("User data is required")
        
        try:
            user_orm = await self.repository.create(User(**user_create.model_dump()))
            return create_ok("User created successfully", UserRead.model_validate(user_orm))
        
        except Exception as e:
            return create_error(f"Error creating user: {e}", 500)
        
# Update an existing user
    async def update_user(self, id: UUID, user_create: UserCreate) -> BaseResponse:
        if id is None:
            return create_error("User ID is required")

        if user_create is None:
            return create_error("User data is required")

        if not self.repository.is_object_exists(id):
            return create_error(f"User with the {id} ID does not exist")

        try:
            user_orm = await self.repository.get(id)

            if user_orm is None:
                return create_error("User not found")

            for key, value in user_create.model_dump().items():
                setattr(user_orm, key, value)

            updated_user_orm = await self.repository.update(user_orm)
            return create_ok("User updated successfully", UserRead.model_validate(updated_user_orm))

        except Exception as e:
            return create_error(f"Error updating user: {e}", 500)
        
# Delete an existing user
    async def delete_user(self, id: UUID) -> BaseResponse:
        
        if id is None:
            return create_error("User ID is required")
        
        if not self.repository.is_object_exists(id):
            return create_error(f"User with the {id} ID does not exist")
        
        try:
            await self.repository.delete(id)
            return create_ok("User deleted successfully")
        
        except Exception as e:
            return create_error(f"Error deleting user: {e}", 500)