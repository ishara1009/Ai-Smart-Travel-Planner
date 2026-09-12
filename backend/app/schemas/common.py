from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class MongoModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T | None = None
    message: str | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    code: str
    details: Any = None


class MessageResponse(BaseModel):
    success: bool = True
    message: str
