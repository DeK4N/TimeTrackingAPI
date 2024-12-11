from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from ..models import Project
from ..schemas import ProjectSchema
from ..database import get_db
import datetime as dt

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

@router.get("/")
async def home(db: Session = Depends(get_db)):
    return db.query(Project).all()

@router.delete('/delete/{project_id}')
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        return {"message": "Project doesn't exists"}
    else:
        db.delete(project)
        db.commit()
        return {"message": "Project deleted successfully"}    
    
@router.post('/create')
async def create_project(request: ProjectSchema, db: Session = Depends(get_db)):
    new_project = Project(
        user_id = request.user_id,
        project_name = request.project_name,
        project_status = request.project_status,
        project_details = request.project_details,
        created_at = str(dt.datetime.now()),
        updated_at = str(dt.datetime.now())
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {"message": "Project created successfully"}

@router.post('/save')
async def save_project(request: ProjectSchema, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == request.project_id).first()
    if project:
        project.project_name = request.project_name
        project.project_status = request.project_status
        project.project_details = request.project_details
        project.updated_at = str(dt.datetime.now())

        db.commit()
        db.refresh(project)
        return {"message": "Project saved successfully"}
    
    return{"message": "There was a problem with saving the project"}