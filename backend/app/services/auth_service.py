from app.core.exceptions import AuthenticationError, ConflictError
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse
from app.schemas.user import UserCreate, UserLogin, UserPublic
from app.utils.response_utils import serialize_document
from pymongo.errors import DuplicateKeyError


def to_public_user(document: dict) -> UserPublic:
    return UserPublic.model_validate(serialize_document(document))


class AuthService:
    def __init__(self, users: UserRepository):
        self.users = users

    async def register(self, payload: UserCreate) -> TokenResponse:
        if await self.users.find_by_email(str(payload.email)):
            raise ConflictError("An account with this email already exists", "EMAIL_EXISTS")
        try:
            document = await self.users.create(payload.name.strip(), str(payload.email), hash_password(payload.password))
        except DuplicateKeyError as exc:
            raise ConflictError("An account with this email already exists", "EMAIL_EXISTS") from exc
        token, expires_in = create_access_token(str(document["_id"]))
        return TokenResponse(access_token=token, expires_in=expires_in, user=to_public_user(document))

    async def login(self, payload: UserLogin) -> TokenResponse:
        document = await self.users.find_by_email(str(payload.email).lower())
        if not document or not verify_password(payload.password, document["password_hash"]):
            raise AuthenticationError("Invalid email or password")
        token, expires_in = create_access_token(str(document["_id"]))
        return TokenResponse(access_token=token, expires_in=expires_in, user=to_public_user(document))
