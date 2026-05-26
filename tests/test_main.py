import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_punch_in_success():
    """Prueba un registro de check-in exitoso."""
    response = client.post(
        "/punch",
        json={"badge_number": "12345", "status": "check-in"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "check-in"

def test_duplicate_punch_fail():
    """Prueba que el sistema bloquea dos registros iguales consecutivos."""
    # Primer registro (debe ser exitoso)
    client.post("/punch", json={"badge_number": "12345", "status": "check-in"})
    
    # Segundo registro igual (debe fallar)
    response = client.post(
        "/punch",
        json={"badge_number": "12345", "status": "check-in"}
    )
    assert response.status_code == 400
    assert "Invalid action" in response.json()["detail"]

def test_invalid_badge():
    """Prueba que un usuario inexistente reciba un 404."""
    response = client.post(
        "/punch",
        json={"badge_number": "99999", "status": "check-in"}
    )
    assert response.status_code == 404