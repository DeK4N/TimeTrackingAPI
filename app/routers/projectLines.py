from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from ..models import ProjectLine
from ..schemas import ProjectLineSchema
from ..database import get_db
import datetime as dt

router = APIRouter(
    prefix="/project-line",
    tags=["project-lines"]
)

@router.get("/")
async def home(db: Session = Depends(get_db)):
    return db.query(ProjectLine).all()

@router.get("/{project_id}")
async def get_project_lines(project_id: int, db: Session = Depends(get_db)):
    return db.query(ProjectLine).filter(ProjectLine.project_id == project_id).all()

@router.post("/create")
async def create_line(request: ProjectLineSchema, db: Session = Depends(get_db)):
    new_line = ProjectLine(
        project_id = request.project_id,
        line_name = request.line_name,
        line_details = request.line_details,
        created_at = str(dt.datetime.now()),
        updated_at = str(dt.datetime.now())
    )

    db.add(new_line)
    db.commit()
    db.refresh(new_line)

    return {"message": "Project line created successfully"}

@router.post("/save")
async def save_lines(request: List[ProjectLineSchema], db: Session = Depends(get_db)):
    for line in request:
        curr_line = db.query(ProjectLine).filter(ProjectLine.id == line.line_id).first()

        if curr_line:
            curr_line.line_name = line.line_name
            curr_line.line_details = line.line_details

            db.commit()
            db.refresh(curr_line)
        
    return {"message": "Projects lines save successfully"}

@router.delete("/delete/{line_id}")
async def delete_line(line_id: int, db: Session = Depends(get_db)):
    line = db.query(ProjectLine).filter(ProjectLine.id == line_id).first()

    if line:
        db.delete(line)
        db.commit()

    return {"message": "Project line deleted successfully"}

