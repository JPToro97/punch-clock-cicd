import os
os.environ["TESTING"] = "True"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool  # <--- NUEVO IMPORT VITAL

from app.main import app, get_db
from app.database import Base
from app import models  # Aseguramos que los modelos estén cargados en memoria

# 1. Configuración de base de datos en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# 2. IMPORTANTE: Agregar StaticPool
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # <--- LA SOLUCIÓN: Mantiene las tablas vivas
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# 3. CREACIÓN DEFINITIVA DE TABLAS
Base.metadata.create_all(bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# --- PRUEBAS UNITARIAS ---

def test_read_employees_empty():
    """Prueba que inicialmente la lista de empleados esté vacía"""
    response = client.get("/employees")
    assert response.status_code == 500
    assert response.json() == []

def test_create_employee():
    """Prueba la creación exitosa de un empleado"""
    response = client.post("/employees", json={"name": "Juan Toro", "badge_number": "12345"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Juan Toro"
    assert data["badge_number"] == "12345"

def test_create_employee_invalid_name():
    """Prueba que falle si el nombre contiene números"""
    response = client.post("/employees", json={"name": "Juan123", "badge_number": "54321"})
    assert response.status_code == 422