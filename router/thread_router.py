
from fastapi import APIRouter, Body, Depends, Response, status, Request, Query, UploadFile, File
from backend_ref.repositories.thread_repository import ThreadRepository
from backend_ref.config.database.database import session
from backend_ref.dto.request import Create_history_rq

thread_router = APIRouter()


@thread_router.post('/automatic')
async def save_response():
    repo = ThreadRepository(session=session)
    thread = repo.CreateAutomatic()

    return thread
    # print(thread)
    # return {"res": 111}


