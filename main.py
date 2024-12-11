from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, TimesheetPeriods
from app.database import engine, SessionLocal
from app.routers import timesheets, timeEntry, projects, projectLines
import datetime
from fastapi.middleware.cors import CORSMiddleware


#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins for production
    allow_credentials=True,
    allow_methods=["*"],  # Allow POST, GET, etc.
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fill_periods():
    db = next(get_db())
    try:
        for month in range(1, 13):
            year = 2024
            start_date = datetime.datetime(year, month, 1)

            # Adjust start_date to the first Monday of the month, if necessary
            if start_date.weekday() != 0:  # 0 represents Monday
                days_to_next_monday = (7 - start_date.weekday()) % 7
                start_date += datetime.timedelta(days=days_to_next_monday)

            last_day_of_month = (start_date.replace(month=month % 12 + 1, day=1) - datetime.timedelta(days=1)).day

            # Loop through the month by week, always starting from a Monday
            current_date = start_date
            while current_date.month == month:
                # Determine the end of the current week (Sunday)
                week_end = current_date + datetime.timedelta(days=6)

                # If week_end extends beyond the end of the month, adjust it
                if week_end.month != month:
                    week_end = datetime.datetime(year, month, last_day_of_month)

                # Create a new TimesheetPeriods record
                new_period = TimesheetPeriods(
                    month_id=current_date.month,
                    start_date=current_date,
                    end_date=week_end,
                    created_at=datetime.datetime.now()
                )

                db.add(new_period)

                # Move to the next week, which starts on the following Monday
                current_date = week_end + datetime.timedelta(days=1)
                if current_date.weekday() != 0:  # Adjust to the next Monday if needed
                    days_to_next_monday = (7 - current_date.weekday()) % 7
                    current_date += datetime.timedelta(days=days_to_next_monday)

        # Commit the changes to save them in the database
        db.commit()

    except Exception as e:
        db.rollback()  # Rollback in case of any error to maintain data consistency
        print(f"An error occurred: {e}")

    finally:
        db.close()

# Call the function to create timesheet periods
fill_periods()
    

app.include_router(timesheets.router)
app.include_router(timeEntry.router)
app.include_router(projects.router)
app.include_router(projectLines.router)

@app.get("/")
async def home():
    return {"message": "Hello World"}

@app.get('/periods')
async def get_periods(db: Session = Depends(get_db)):
    return db.query(TimesheetPeriods).all()