from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user_id
from app.main import app


def test_root_is_available():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "AI Smart Travel Planner"


def test_protected_route_requires_token():
    client = TestClient(app)
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert response.json()["code"] == "AUTHENTICATION_ERROR"
