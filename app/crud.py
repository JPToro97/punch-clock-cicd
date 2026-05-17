from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException, status
from . import models, schemas

def register_punch(db: Session, punch: schemas.PunchCreate):
    # 1. Verify if the employee exists by their badge number
    employee = db.query(models.Employee).filter(models.Employee.badge_number == punch.badge_number).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Employee badge number not recognized."
        )

    # 2. Query the last punch registration for this specific employee
    last_log = db.query(models.PunchLog)\
                 .filter(models.PunchLog.employee_id == employee.id)\
                 .order_by(desc(models.PunchLog.timestamp))\
                 .first()

    # 3. State Validation Logic: Check against duplicate consecutive states
    if last_log and last_log.status == punch.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid action. Your last registered status is already '{punch.status}'."
        )

    # 4. Save the new valid punch log to the database
    new_log = models.PunchLog(
        employee_id=employee.id,
        status=punch.status
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log