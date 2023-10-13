from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
import io
import os
import datetime
from backend_ref.config.database.database import DatabaseSession
from helper.help import GetRootDir, rootDir
from sqlalchemy.orm import Session
from backend_ref.config.database.database import session
from backend_ref.repositories.models import history, thread

display_router = APIRouter()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@display_router.get('/chat_history')
async def display_hi(date: str, db: session = Depends(DatabaseSession.GetDatabaseInfo())):
    try:
        # Convert the date parameter to a datetime object
        date_datetime = datetime.strptime(date, "%d/%m/%Y")

        # Query the database for chat history on the specified date
        _history = db.query(history).filter(
            history.title >= date_datetime,
            history.title < date_datetime + timedelta(days=1)
        ).all()
        return history
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
