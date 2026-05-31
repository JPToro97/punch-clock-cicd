import pytest
# Change this import
from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

def test_punch_in_success():
    # This must match schemas.py: employee_id (str) and status (Literal)
    payload = {
        "employee_id": "12345", 
        "status": "check-in"
    }
    response = client.post("/punch", json=payload)
    
    # Debug print if it fails
    if response.status_code != 200:
        print(response.json())
        
    assert response.status_code == 200