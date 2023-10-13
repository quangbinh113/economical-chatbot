from fastapi import APIRouter, Body, Depends, Response, status, Request, Query, UploadFile, File
from starlette.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from src.model.model import HandleQA
from config.config import config
import os 
from src.getdata.user_query import get_data
from fastapi.responses import StreamingResponse
from src.getdata.crawler.file_loader import FileLoader
ai_router = APIRouter()
DOCUMENTS_PATH = 'file_upload'
chat = HandleQA(config)

class AIResponseModel(BaseModel):
    cau_tra_loi: Optional[str]


class AIQueryModel(BaseModel):
    question: str
    documents: str | None = None


@ai_router.post('/get_response')
async def get_response(input_: AIQueryModel):
    questionUser = input_.question
    out = AIResponseModel(cau_tra_loi=None)
    chat.reset_callback()
    if input_.documents:
        file_loader = FileLoader()
        documents = file_loader.load_file(os.path.join(DOCUMENTS_PATH,input_.documents))
        generator = chat.ask_gpt(questionUser,documents = documents)
    else:     
        crawl_data = get_data(questionUser) 
        generator = chat.ask_gpt(questionUser,crawl_data=crawl_data)

    return StreamingResponse(generator, media_type="text/event-stream")
    
    # out.cau_tra_loi = fr'{str(x)}'

    # return out