from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)

class Timesheet(Base):
    __tablename__ = "timesheets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    year = Column(Integer, index=True)
    month = Column(String, index=True)
    status = Column(String, index=True)
    created_at = Column(String, index=True)
    updated_at = Column(String, index=True)

class TimesheetEntry(Base):
    __tablename__ = "timesheet_entry"
    id = Column(Integer, primary_key=True, index=True)
    timesheet_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    project_id = Column(Integer, index=True)
    project_line_id = Column(Integer, index=True)
    ticket = Column(String, index=True)
    time_spent = Column(Integer, index=True)
    notes = Column(String, index=True)
    date = Column(String, index=True)
    created_at = Column(String, index=True)
    updated_at = Column(String, index=True)

class TimesheetPeriods(Base):
    __tablename__ = "timesheet_periods"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    month_id = Column(Integer, index=True)
    start_date = Column(String, index=True)
    end_date = Column(String, index=True)
    created_at = Column(String, index=True)

class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    project_name = Column(String, index=True)
    project_status = Column(String, index=True)
    project_details = Column(String, index=True)
    created_at = Column(String, index=True)
    updated_at = Column(String, index=True)

class ProjectLine(Base):
    __tablename__ = 'project_line'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    line_name = Column(String, index=True)
    line_details = Column(String, index=True)
    created_at = Column(String, index=True)
    updated_at = Column(String, index=True)
