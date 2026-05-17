from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import models, schemas, crud

# Automatically construct database tables inside PostgreSQL if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Punch-Clock System V1")

# Seed basic data so the database isn't empty when testing
@app.on_event("startup")
def seed_database():
    db = next(get_db())
    if not db.query(models.Employee).first():
        demo_worker = models.Employee(name="Juan Toro", badge_number="12345")
        db.add(demo_worker)
        db.commit()

@app.get("/")
def home():
    return {"message": "Punch-Clock API is running natively within Docker Compose!"}

@app.post("/punch", response_model=schemas.PunchLogResponse)
def punch_in_out(punch: schemas.PunchCreate, db: Session = Depends(get_db)):
    return crud.register_punch(db=db, punch=punch)

@app.get("/logs/{badge_number}")
def get_employee_logs(badge_number: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.badge_number == badge_number).first()
    if not employee:
        return {"error": "Employee not found"}
    return {"employee": employee.name, "history": employee.logs}