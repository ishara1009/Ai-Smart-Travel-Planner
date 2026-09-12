from fastapi import APIRouter, status

from app.api.dependencies import DatabaseDep
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, database: DatabaseDep) -> TokenResponse:
    return await AuthService(UserRepository(database)).register(payload)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, database: DatabaseDep) -> TokenResponse:
    return await AuthService(UserRepository(database)).login(payload)
