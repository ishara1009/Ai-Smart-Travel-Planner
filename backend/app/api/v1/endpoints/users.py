from fastapi import APIRouter

from app.api.dependencies import CurrentUserId, DatabaseDep
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserPublic, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserPublic)
async def current_user(user_id: CurrentUserId, database: DatabaseDep) -> UserPublic:
    return await UserService(UserRepository(database)).get(user_id)


@router.patch("/me", response_model=UserPublic)
async def update_current_user(payload: UserUpdate, user_id: CurrentUserId, database: DatabaseDep) -> UserPublic:
    return await UserService(UserRepository(database)).update(user_id, payload)
