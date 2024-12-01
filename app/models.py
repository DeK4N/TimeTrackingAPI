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

class KantataProject(Base):
    __tablename__ = "kantata_project"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Integer, index=True)
    created_at = Column(String, index=True)
    updated_at = Column(String, index=True)

class BondProject(Base):
    __tablename__ = "bond_project"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_active = Column(Integer, index=True)
    created_at = Column(String, index=True)
    updated_at = Column(String, index=True)

class TimesheetEntry(Base):
    __tablename__ = "timesheet_entry"
    id = Column(Integer, primary_key=True, index=True)
    timesheet_id = Column(Integer, index=True)
    bond_project_id = Column(Integer, index=True)
    kantata_project_id = Column(Integer, index=True)
    zendesk_ticket = Column(String, index=True)
    note = Column(String, index=True)
    entry_date = Column(String, index=True)
    time = Column(Integer, index=True)
    created_at = Column(String, index=True)
    updated_at = Column(String, index=True)

class TimesheetPeriods(Base):
    __tablename__ = "timesheet_periods"
    id = Column(Integer, primary_key=True, index=True)
    month_id = Column(Integer, index=True)
    start_date = Column(String, index=True)
    end_date = Column(String, index=True)
    created_at = Column(String, index=True)