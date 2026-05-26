import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_punch_in_success():
    """Verify that a valid check-in request is processed successfully."""
    response = client.post(
        "/punch",
        json={"badge_number": "12345", "status": "check-in"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "check-in"

def test_duplicate_punch_fail():
    """Verify that the system prevents consecutive identical punch actions."""
    # First request (successful)
    client.post("/punch", json={"badge_number": "12345", "status": "check-in"})
    
    # Second request (must return 400 Bad Request)
    response = client.post(
        "/punch",
        json={"badge_number": "12345", "status": "check-in"}
    )
    assert response.status_code == 400
    assert "Invalid action" in response.json()["detail"]

def test_invalid_badge():
    """Verify that an unknown badge number returns a 404 error."""
    response = client.post(
        "/punch",
        json={"badge_number": "99999", "status": "check-in"}
    )
    assert response.status_code == 404