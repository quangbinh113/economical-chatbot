from fastapi import APIRouter, Body, Depends, Response, HTTPException, status, Request, Query, UploadFile, File
from backend_ref.repositories.thread_repository import ThreadRepository
from backend_ref.config.database.database import session
from backend_ref.repositories.history_repository import HistoryRepository
from backend_ref.dto.request import CreateHistoryRequest, SaveClickResponse
from backend_ref.dto.response import CreateHistoryResponse
from sqlalchemy.orm import Session

history_router = APIRouter()


@history_router.post('/automaticQA')
async def save_response(request: SaveClickResponse):
    try:
        repo = HistoryRepository(session=session)
        html = None
        print('request: ', request)
        if request.answer.metadata is not None:
            html = request.answer.metadata["location"]

        history = repo.auto_fill_qa(message=request.question,  answer=request.answer.content, location_html=html)
        print('history: ', history)
        print(f'{history.answer}')
        return CreateHistoryRequest(question=history.message, answer=history.answer, location_html=history.location_html, created_at=history.created_at,
                                        updated_at=history.updated_at, title=history.title, topic=history.thread.topic)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.__str__())


@history_router.get('/get_history_thread')
async def get_history(request: str):
    repo = HistoryRepository(session=session)
    return repo.load_all_by_thread(request)
