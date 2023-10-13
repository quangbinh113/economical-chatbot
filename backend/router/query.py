from fastapi import APIRouter, Body, Depends, Response, status, Request, Query, UploadFile, File
from starlette.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from src.model.model import HandleQA
from config.config import config
import os
from src.getdata.user_query import get_data
from router.history_router import history_router
from router.thread_router import thread_router
from router.save_history_click import history_click
from database.schemas import AIQueryModel, AIResponseModel


ai_router = APIRouter()
chat = HandleQA(config)
ai_router.include_router(thread_router, prefix="/thread")
ai_router.include_router(history_router, prefix="/history")
ai_router.include_router(history_click, prefix="/history_click")


@ai_router.post('/get_response')
async def get_response(input_model: AIQueryModel):
    # path = 'data/data'
    # chat = HandleQA(config)
    question_user = input_model.question
    out = AIResponseModel(response=None)
    documents = get_data(question_user)
    response_gpt = chat.ask_gpt(question_user,documents)
    # code logic de tra ve cau tra loi
    # crawl data tu html -> file texts -> tong hop cau tra loi -> dua ra cau dung nhat = AI model sau do gan vao response message
    # dataCanXuLy = 'bla bla'  # can xu dung logic cua AI
    out.response = fr'{str(response_gpt)}'
    return out