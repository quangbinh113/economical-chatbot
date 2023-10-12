from fastapi import APIRouter, Body, Depends, Response, HTTPException, status, Request, Query, UploadFile, File
from backend_ref.repositories.thread_repository import ThreadRepository
from backend_ref.config.database.database import session
from backend_ref.repositories.history_repository import HistoryRepository
from backend_ref.dto.request import CreateHistoryRequest
from backend_ref.dto.response import CreateHistoryResponse
from backend_ref.dto.request import SaveClickResponse

history_click = APIRouter()


@history_click.post('/save_click')
async def save_response(request: SaveClickResponse):
    try:
        repo = HistoryRepository(session=session)
        history = repo.auto_fill_qa(message=request.question, answer=request.answer)
        # print(f'{history.answer}')
        return CreateHistoryRequest(question=history.message, answer=history.answer, created_at=history.created_at,
                                       updated_at=history.updated_at, title=history.title, topic=history.thread.topic)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.__str__())


@history_click.get('/get_history_thread')
async def get_history(request: str):
    repo = HistoryRepository(session=session)
    return repo.load_all_by_thread(request)
