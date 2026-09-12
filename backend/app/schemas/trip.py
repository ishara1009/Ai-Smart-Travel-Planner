from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator

from app.schemas.itinerary import BudgetAnalysis, ItineraryResult, Recommendation, WeatherSummary


class TripStatus(StrEnum):
    DRAFT = "draft"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    MODIFYING = "modifying"
    COMPLETED = "completed"
    FAILED = "failed"


class TravelRequest(BaseModel):
    destination: str = Field(min_length=2, max_length=120)
    start_date: date
    days: int = Field(ge=1, le=30)
    travelers: int = Field(ge=1, le=50)
    budget: float = Field(gt=0, le=100_000_000)
    currency: str = Field(default="LKR", min_length=3, max_length=3)
    interests: list[str] = Field(default_factory=list, max_length=12)
    transport_preferences: list[str] = Field(default_factory=list, max_length=8)
    accommodation_preference: str | None = Field(default=None, max_length=100)
    food_preference: str | None = Field(default=None, max_length=100)
    activity_preferences: list[str] = Field(default_factory=list, max_length=12)
    special_requirements: str | None = Field(default=None, max_length=1000)
    user_query: str | None = Field(default=None, max_length=2000)

    @field_validator("destination")
    @classmethod
    def clean_destination(cls, value: str) -> str:
        return " ".join(value.split())

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()


class ModifyTripRequest(BaseModel):
    instructions: str = Field(min_length=3, max_length=2000)


class FeedbackCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=2000)


class TripPublic(BaseModel):
    id: str
    user_id: str
    destination: str
    start_date: date
    days: int
    travelers: int
    budget: float
    currency: str
    interests: list[str] = []
    transport_preferences: list[str] = []
    accommodation_preference: str | None = None
    food_preference: str | None = None
    activity_preferences: list[str] = []
    special_requirements: str | None = None
    status: TripStatus
    weather: WeatherSummary | None = None
    budget_analysis: BudgetAnalysis | None = None
    recommendations: list[Recommendation] = []
    itinerary: ItineraryResult | None = None
    warnings: list[str] = []
    created_at: datetime
    updated_at: datetime
