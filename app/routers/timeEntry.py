from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from ..models import TimesheetEntry
from ..schemas import TimesheetEntrySchema, TimesheetEntrySaveSchema, FieldUpdate
from ..database import get_db
import datetime as dt

router = APIRouter(
    prefix="/timesheet-entries",
    tags=["timesheet-entries"]
)


def serialize_sqlalchemy_obj(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


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
        notes = request.notes,
        date = request.date,
        created_at = str(dt.datetime.now()),
        updated_at = str(dt.datetime.now())
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return JSONResponse(
        content={
            "message": "New time entry added successfully",
            "entry": serialize_sqlalchemy_obj(new_entry)
        },
        status_code=201,
    )


# @router.put("/save/{time_entry_id}")
# async def save_timesheet_entry(request: TimesheetEntrySaveSchema, time_entry_id: int, db: Session = Depends(get_db)):
#     entry = db.query(TimesheetEntry).filter(TimesheetEntry.id == time_entry_id).first()

#     if entry and entry.id == request.id:
#         entry.project_id = request.project_id
#         entry.project_line_id = request.project_line_id
#         entry.ticket = request.ticket
#         entry.time_spent = request.time_spent
#         entry.notes= request.notes
#         entry.date = request.date

#         db.commit()
#         db.refresh(entry)

#         return {"message": "Time entry saved successfully"}
#     else:
#         return {"message": "There was a problem with saving the time entry"}
    
@router.delete("/delete/{time_entry_id}")
async def delete_timesheet_entry(time_entry_id: int, db:Session = Depends(get_db)):
    entry = db.query(TimesheetEntry).filter(TimesheetEntry.id == time_entry_id).first()

    if entry:
        db.delete(entry)
        db.commit()
        return {"message": "Time entry deleted successfully"}
    else:
        return {"message": "There was a problem when deleting the time entry"}


@router.put("/update/{time_entry_id}")
async def update_entry(time_entry_id: int, response: FieldUpdate, db: Session = Depends(get_db)):
    entry = db.query(TimesheetEntry).filter(TimesheetEntry.id == time_entry_id).first()

    if not entry:
        return {"message": "There was a problem when updating the time entry"}

    setattr(entry, response.field_name, response.value)

    db.commit()
    db.refresh(entry)

    return {"message": "Time entry updated successfully"}