from app.core.exceptions import NotFoundError
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserPublic, UserUpdate
from app.services.auth_service import to_public_user


class UserService:
    def __init__(self, users: UserRepository):
        self.users = users

    async def get(self, user_id: str) -> UserPublic:
        document = await self.users.find_by_id(user_id)
        if not document:
            raise NotFoundError("User not found", "USER_NOT_FOUND")
        return to_public_user(document)

    async def update(self, user_id: str, payload: UserUpdate) -> UserPublic:
        changes = payload.model_dump(exclude_none=True)
        document = await self.users.update(user_id, changes)
        if not document:
            raise NotFoundError("User not found", "USER_NOT_FOUND")
        return to_public_user(document)
