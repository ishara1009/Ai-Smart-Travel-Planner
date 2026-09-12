from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pymongo.asynchronous.database import AsyncDatabase

from app.core.exceptions import AuthenticationError, ExternalServiceError
from app.core.security import decode_access_token
from app.db.mongodb import mongo

bearer = HTTPBearer(auto_error=False)


def get_database(request: Request) -> AsyncDatabase:
    if not getattr(request.app.state, "database_ready", False):
        raise ExternalServiceError("database", "Database is temporarily unavailable")
    return mongo.get_database()


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError()
    user_id = decode_access_token(credentials.credentials)
    if not user_id:
        raise AuthenticationError()
    return user_id


DatabaseDep = Annotated[AsyncDatabase, Depends(get_database)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]
