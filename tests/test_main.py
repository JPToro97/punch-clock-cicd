import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base

# 1. Configuración de una base de datos SQLite en memoria exclusiva para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Reemplazamos la dependencia de la base de datos real por la de pruebas
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Fixture para crear y destruir las tablas antes y después de cada prueba
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# --- PRUEBAS UNITARIAS ---

def test_read_employees_empty():
    """Prueba que inicialmente la lista de empleados esté vacía"""
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json() == []

def test_create_employee():
    """Prueba la creación exitosa de un empleado respetando las validaciones"""
    response = client.post("/employees", json={"name": "Juan Toro", "badge_number": "12345"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Juan Toro"
    assert data["badge_number"] == "12345"

def test_create_employee_invalid_name():
    """Prueba que falle si el nombre contiene números (Validación Pydantic/JS)"""
    response = client.post("/employees", json={"name": "Juan123", "badge_number": "54321"})
    # Cambia a 422 (Unprocessable Entity) debido a las restricciones de Pydantic
    assert response.status_code == 422