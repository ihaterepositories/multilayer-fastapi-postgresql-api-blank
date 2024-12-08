from fastapi import Depends, APIRouter, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.data.database import get_db
from app.data.schemas.user_schemas import UserCreate
from app.utils.responding.models.base_response import BaseResponse
from app.services.user_service import UserService

user_router = APIRouter()

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

@user_router.get("/users", response_model=BaseResponse)
async def read_users(
    sort: str = Query(None, description="Sort options (leave empty for no sorting) : name, email"), 
    order: int = Query(1, description="Sort order: 1 for ascending, -1 for descending"), 
    skip: int = Query(0, description="Skip some count of first users"), 
    limit: int = Query(0, description="Limit the number of users (0 - no limit)"), 
    service: UserService = Depends(get_user_service)):
    return await service.get_users(sort, order, skip, limit)

@user_router.get("/user", response_model=BaseResponse)
async def read_user(
    user_id: UUID = Query(..., description="User ID"),
    service: UserService = Depends(get_user_service)):
    return await service.get_user(user_id)

@user_router.post("/users", response_model=BaseResponse)
async def create_user(
    user: UserCreate = Body(..., embed=True), 
    service: UserService = Depends(get_user_service)):
    return await service.create_user(user)

@user_router.put("/users", response_model=BaseResponse)
async def update_user(
    user_id: UUID = Query(..., description="User ID"),
    user: UserCreate = Body(..., embed=True), 
    service: UserService = Depends(get_user_service)):
    return await service.update_user(user_id, user)

@user_router.delete("/users", response_model=BaseResponse)
async def delete_user(
    user_id: UUID = Query(..., description="User ID"),
    service: UserService = Depends(get_user_service)):
    return await service.delete_user(user_id)