from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..models import Timesheet
from ..schemas import TimesheetSchema
from ..database import get_db

router = APIRouter(
    prefix="/timesheets",
    tags=["timesheets"]
)

@router.get("/")
async def home(db: Session = Depends(get_db)):
    return db.query(Timesheet).all()

@router.get("/{timesheet_id}")
async def get_timesheet(timesheet_id: int, db: Session = Depends(get_db)):
    return db.query(Timesheet).filter(Timesheet.id == timesheet_id).first()

@router.post('/create')
async def add_timesheet(request: TimesheetSchema, db: Session = Depends(get_db)):
    timesheet = Timesheet(
        user_id=request.user_id,
        month=request.month,
        year=request.year,
        status=request.status, 
        created_at=request.created_at, 
        updated_at=request.updated_at
    )

    db.add(timesheet)
    db.commit()
    db.refresh(timesheet)

    return timesheet


@router.post('/delete/{timesheet_id}')
async def delete_timesheet(timesheet_id: int, db: Session = Depends(get_db)):
    timesheet = db.query(Timesheet).filter(Timesheet.id == timesheet_id).first()
    if timesheet is None:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    db.delete(timesheet)
    db.commit()

    return JSONResponse(content={"status": "OK", "message": "Request successful"}, status_code=200)
        

@router.get('/details/{timesheet_id}')
async def get_timesheet_details(timesheetid: int, db: Session = Depends(get_db)):
    timesheet = db.query(Timesheet).filter(Timesheet.id == timesheetid).first()
    if timesheet is None:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    
    return timesheet


