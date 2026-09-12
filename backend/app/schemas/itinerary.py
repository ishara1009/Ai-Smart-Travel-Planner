from typing import Annotated
from urllib.parse import urlparse

from pydantic import AfterValidator, BaseModel, Field


def validate_source_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Source URL must be an absolute HTTP(S) URL")
    return value


SourceUrl = Annotated[str, AfterValidator(validate_source_url)]


class WeatherSummary(BaseModel):
    available: bool = False
    location: str | None = None
    observed_at: str | None = None
    temperature_c: float | None = None
    condition: str | None = None
    humidity: int | None = None
    wind_kph: float | None = None
    precipitation_mm: float | None = None
    limitation: str | None = None


class BudgetCategory(BaseModel):
    name: str
    estimated_amount: float = Field(ge=0)
    note: str = "Estimated; verify before travel"


class BudgetAnalysis(BaseModel):
    total_budget: float
    estimated_total: float
    remaining_budget: float
    within_budget: bool
    currency: str
    categories: list[BudgetCategory]
    is_estimate: bool = True


class SearchResult(BaseModel):
    title: str
    url: SourceUrl
    content: str
    score: float | None = None


class Recommendation(BaseModel):
    name: str
    reason: str
    category: str
    estimated_cost: float | None = None
    source_url: SourceUrl | None = None


class Activity(BaseModel):
    time: str
    title: str
    description: str = ""
    reason: str
    estimated_cost: float | None = None
    weather_consideration: str | None = None
    transport_note: str | None = None
    source_url: SourceUrl | None = None


class DayPlan(BaseModel):
    day: int = Field(ge=1)
    date: str
    theme: str
    activities: list[Activity]
    estimated_daily_cost: float = Field(ge=0)


class ItineraryResult(BaseModel):
    title: str
    summary: str
    days: list[DayPlan]
    estimated_total: float = Field(ge=0)
    currency: str
    sources: list[SourceUrl] = []
    warnings: list[str] = []


class ValidationResult(BaseModel):
    valid: bool
    errors: list[str] = []
    warnings: list[str] = []
    needs_replan: bool = False
