from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    email: str
    password: str


class TimesheetSchema(BaseModel):
    user_id: int
    year: int
    month: str
    status: str
    created_at: str
    updated_at: str

class KantaProjectSchema(BaseModel):
    name: str
    is_active: int
    created_at: str
    updated_at: str

class BondProjectSchema(BaseModel):
    name: str
    is_active: int
    created_at: str
    updated_at: str

class TimesheetEntrySchema(BaseModel):
    timesheet_id: int
    bond_project_id: int
    kantata_project_id: int
    zendesk_ticket: str
    note: str
    entry_date: str
    time: int
    created_at: str
    updated_at: str