from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException, status

def register_punch(db: Session, punch: schemas.PunchCreate):
    # 1. Find Employee
    employee = db.query(models.Employee).filter(models.Employee.badge_number == punch.badge_number).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee = db.query(models.Employee).filter(models.Employee.badge_number == punch.badge_number).first()
    print(f"DEBUG: Found employee ID {employee.id if employee else 'NONE'}")
    # 2. Get last punch
    last_punch = db.query(models.PunchLog).filter(models.PunchLog.employee_id == employee.id).order_by(models.PunchLog.timestamp.desc()).first()
    last_status = last_punch.status if last_punch else None

    # 3. Validation Logic
    if punch.status == "check-in" and last_status == "check-in":
        raise HTTPException(status_code=400, detail="Already checked in!")
    
    if punch.status in ["break", "check-out"] and last_status != "check-in":
        raise HTTPException(status_code=400, detail="You must check-in first!")

    # 4. Save
    db_punch = models.PunchLog(employee_id=employee.id, status=punch.status)
    db.add(db_punch)
    db.commit()
    return db_punch

def get_employees(db: Session):
    return db.query(models.Employee).all()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(name=employee.name, badge_number=employee.badge_number)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee

def get_employee_history(db: Session, badge_number: str):
    employee = db.query(models.Employee).filter(models.Employee.badge_number == badge_number).first()
    if not employee:
        return None
    # Return all logs for this employee, ordered by newest first
    return db.query(models.PunchLog).filter(models.PunchLog.employee_id == employee.id).order_by(models.PunchLog.timestamp.desc()).all()