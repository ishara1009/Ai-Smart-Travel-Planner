from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    travel_interests: list[str] | None = None
    default_currency: str | None = Field(default=None, min_length=3, max_length=3)
    travel_style: str | None = Field(default=None, max_length=50)
    preferred_accommodation: str | None = Field(default=None, max_length=80)
    preferred_transport: list[str] | None = None

    @field_validator("default_currency")
    @classmethod
    def uppercase_currency(cls, value: str | None) -> str | None:
        return value.upper() if value else value


class UserPublic(BaseModel):
    id: str
    name: str
    email: EmailStr
    travel_interests: list[str] = []
    default_currency: str = "LKR"
    travel_style: str | None = None
    preferred_accommodation: str | None = None
    preferred_transport: list[str] = []
    created_at: datetime
    updated_at: datetime
