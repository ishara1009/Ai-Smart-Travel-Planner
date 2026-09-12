from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.schemas.trip import TravelRequest
from app.models.trip import new_trip_document
from bson import ObjectId


def test_travel_request_normalizes_destination_and_currency():
    request = TravelRequest(destination="  Kandy   Sri Lanka ", start_date=date.today() + timedelta(days=1), days=3, travelers=2, budget=60000, currency="lkr")
    assert request.destination == "Kandy Sri Lanka"
    assert request.currency == "LKR"


def test_travel_request_rejects_invalid_days():
    with pytest.raises(ValidationError):
        TravelRequest(destination="Kandy", start_date=date.today(), days=0, travelers=2, budget=60000)


def test_trip_document_uses_bson_safe_iso_date():
    request = TravelRequest(destination="Kandy", start_date=date(2026, 10, 10), days=3, travelers=2, budget=60000)
    document = new_trip_document(str(ObjectId()), request)
    assert document["start_date"] == "2026-10-10"
