from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.db import get_db
from api.models import Appointment


class AppointmentCreate(BaseModel):
    patient_name: str = Field(min_length=1, max_length=120)
    appointment_type: str = Field(min_length=1, max_length=120)
    appointment_time: str = Field(min_length=1, max_length=64)
    notes: str = Field(default="", max_length=500)


class AppointmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_name: str
    appointment_type: str
    appointment_time: str
    status: str
    notes: str


router = APIRouter()


@router.get("/appointments", response_model=list[AppointmentOut])
def list_appointments(db: Session = Depends(get_db)) -> list[Appointment]:
    return list(db.scalars(select(Appointment).order_by(Appointment.id.desc())).all())


@router.post("/appointments", response_model=AppointmentOut, status_code=201)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)) -> Appointment:
    appt = Appointment(**payload.model_dump(), status="booked")
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


@router.post("/appointments/{appointment_id}/reschedule", response_model=AppointmentOut)
def reschedule_appointment(appointment_id: int, payload: AppointmentCreate, db: Session = Depends(get_db)) -> Appointment:
    appt = db.get(Appointment, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appt.patient_name = payload.patient_name
    appt.appointment_type = payload.appointment_type
    appt.appointment_time = payload.appointment_time
    appt.notes = payload.notes
    appt.status = "rescheduled"
    db.commit()
    db.refresh(appt)
    return appt
