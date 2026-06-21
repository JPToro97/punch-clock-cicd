from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    badge_number = Column(String, unique=True, index=True)
    
    # Relación bidireccional
    punch_logs = relationship("PunchLog", back_populates="employee", cascade="all, delete-orphan")


class PunchLog(Base):
    __tablename__ = "punch_logs"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relación bidireccional
    employee = relationship("Employee", back_populates="punch_logs")

    # Propiedad dinámica para satisfacer el esquema Pydantic
    @property
    def badge_number(self):
        return self.employee.badge_number if self.employee else None