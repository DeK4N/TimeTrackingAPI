from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..models import TimesheetEntry
from ..schemas import TimesheetEntrySchema
from ..database import get_db

router = APIRouter(
    prefix="/timesheet-entries",
    tags=["timesheet-entries"]
)

@router.get("/")
async def home(db: Session = Depends(get_db)):
    return db.query(TimesheetEntry).all()

@router.get("/{timesheet_id}")
async def home(timesheet_id: int, db: Session = Depends(get_db)):
    data = db.query(TimesheetEntry).filter(TimesheetEntry.timesheet_id == timesheet_id).all()

    if data:
        return data
    else:
        return {"message": "Error when getting time entries"}

@router.post("/create")
async def add_timesheet_entry(request: TimesheetEntrySchema, db: Session = Depends(get_db)):
    new_entry = TimesheetEntry(
        timesheet_id = request.timesheet_id,
        user_id = request.user_id,
        project_id = request.project_id,
        project_line_id = request.project_line_id,
        ticket = request.ticket,
        time_spent = request.time_spent,
        notes = request.notes
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {"message": "New time entry added successfully"}