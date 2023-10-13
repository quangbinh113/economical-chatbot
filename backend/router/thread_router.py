from fastapi import APIRouter, Body, Depends, Response, status, Request, Query, UploadFile, File
from backend_ref.repositories.thread_repository import ThreadRepository
from backend_ref.config.database.database import session
from backend_ref.dto.request import CreateHistoryRequest
from backend_ref.dto.response import ThreadItem
import traceback

thread_router = APIRouter()


@thread_router.post('/automatic')
async def save_response():
    repo = ThreadRepository(session=session)
    thread = repo.create_automatic()
    return thread


@thread_router.get('/get_thread')
async def get_thread():
    list_thread = []
    repo = ThreadRepository(session=session)
    try:
        thread = repo.load_all()
        for item in thread:
            _item = ThreadItem(id=item.id, topic=item.topic, created_at=item.created_at, updated_at=item.updated_at)
            list_thread.append(_item)
    except Exception:
        print("Loi o day")
        traceback.print_exc()

    return list_thread
