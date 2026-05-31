from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException, status

def register_punch(db: Session, punch: schemas.PunchCreate):
    # Logic for registering a punch in the database
    db_punch = models.PunchLog(**punch.dict())
    db.add(db_punch)
    db.commit()
    db.refresh(db_punch)
    return db_punch