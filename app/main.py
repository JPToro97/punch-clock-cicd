from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import models, schemas, crud
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

import os

# Cambia la línea directa por este condicional:
if os.getenv("TESTING") != "True":
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Punch-Clock System V1")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/punch", response_model=schemas.PunchLogResponse)
def punch_in_out(punch: schemas.PunchCreate, db: Session = Depends(get_db)):
    return crud.register_punch(db=db, punch=punch)

@app.get("/", include_in_schema=False)
def redirect_to_dashboard():
    return RedirectResponse(url="/static/index.html")

@app.post("/punch", response_model=schemas.PunchLogResponse)
def punch_in_out(punch: schemas.PunchCreate, db: Session = Depends(get_db)):
    return crud.register_punch(db=db, punch=punch)

@app.get("/logs/{badge_number}")
def get_employee_logs(badge_number: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.badge_number == badge_number).first()
    if not employee:
        return {"error": "Employee not found"}
    return {"employee": employee.name, "history": employee.logs}

@app.get("/employees", response_model=list[schemas.EmployeeResponse])
def read_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

@app.post("/employees", response_model=schemas.EmployeeResponse)
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)

@app.delete("/employees/{employee_id}")
def remove_employee(employee_id: int, db: Session = Depends(get_db)):
    success = crud.delete_employee(db, employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}

@app.get("/history/{badge_number}")
def get_history(badge_number: str, db: Session = Depends(get_db)):
    history = crud.get_employee_history(db, badge_number)
    if not history:
        raise HTTPException(status_code=404, detail="No history found")
    return history