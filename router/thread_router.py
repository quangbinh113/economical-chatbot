from fastapi import APIRouter, Body, Depends, Response, status, Request, Query, UploadFile, File
from backend_ref.repositories.thread_repository import ThreadRepository
from backend_ref.config.database.database import session
from backend_ref.dto.request import Create_history_rq
from backend_ref.dto.responed import thread_item
import traceback

thread_router = APIRouter()


@thread_router.post('/automatic')
async def save_response():
    repo = ThreadRepository(session=session)
    thread = repo.CreateAutomatic()

    return thread
    # print(thread)
    # return {"res": 111}


@thread_router.get('/get_thread')
async def get_thread():
    list_thread = []
    repo = ThreadRepository(session=session)
    try:
        thread = repo.LoadAll()
        for item in thread:
            _item = thread_item(id=item.id, topic=item.topic, created_at=item.created_at, updated_at=item.updated_at)
            list_thread.append(_item)
    except Exception:
        print("Loi o day")
        traceback.print_exc()

    return list_thread
