import pytest

from app.core.exceptions import AuthenticationError, ConflictError
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import AuthService


class FakeUsers:
    def __init__(self): self.user = None
    async def find_by_email(self, email): return self.user if self.user and self.user["email"] == email else None
    async def create(self, name, email, password_hash):
        from datetime import datetime, timezone
        from bson import ObjectId
        now = datetime.now(timezone.utc); self.user = {"_id": ObjectId(), "name": name, "email": email, "password_hash": password_hash, "travel_interests": [], "default_currency": "LKR", "preferred_transport": [], "created_at": now, "updated_at": now}; return self.user


@pytest.mark.asyncio
async def test_register_and_login():
    repo = FakeUsers(); service = AuthService(repo)
    registered = await service.register(UserCreate(name="A Traveler", email="TEST@example.com", password="strongpass"))
    logged_in = await service.login(UserLogin(email="test@example.com", password="strongpass"))
    assert registered.user.email == "test@example.com"
    assert logged_in.access_token


@pytest.mark.asyncio
async def test_duplicate_registration_and_bad_password():
    repo = FakeUsers(); service = AuthService(repo); payload = UserCreate(name="Traveler", email="test@example.com", password="strongpass")
    await service.register(payload)
    with pytest.raises(ConflictError): await service.register(payload)
    with pytest.raises(AuthenticationError): await service.login(UserLogin(email="test@example.com", password="wrongpass"))
