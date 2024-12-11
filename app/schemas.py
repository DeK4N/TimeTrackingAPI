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

class ProjectSchema(BaseModel):
    project_id: int | None = None
    user_id: int | None = None
    project_name: str | None = None
    project_status: str | None = None
    project_details: str | None = None

class TimesheetEntrySchema(BaseModel):
    timesheet_id: int | None = None
    user_id: int | None = None
    project_id: int | None = None
    project_line_id: int | None = None
    ticket: str | None = None
    time_spent: int | None = None
    notes: str | None = None

class ProjectLineSchema(BaseModel):
    line_id: int | None = None
    project_id: int
    line_name: str | None = None
    line_details: str | None = None