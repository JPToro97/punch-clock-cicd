from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import models, schemas, crud
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Ensure database tables exist
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