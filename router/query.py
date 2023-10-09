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

ai_router = APIRouter()

chat = HandleQA(config)
ai_router.include_router(thread_router, prefix="/thread")
ai_router.include_router(history_router, prefix="/history")
ai_router.include_router(history_click, prefix="/history_click")


class AIResponseModel(BaseModel):

    cau_tra_loi: Optional[str]


class AIQueryModel(BaseModel):
    question: str


@ai_router.post('/get_response')
async def get_response(input_: AIQueryModel):
    # path = 'data/data'
    # chat = HandleQA(config)
    questionUser = input_.question
    out = AIResponseModel(cau_tra_loi=None)
    
    documents = get_data(questionUser)
    # files = os.listdir(path)
    # files = [os.path.join(path,file) for file in files]
    
    x = chat.ask_gpt(questionUser,documents)


    # code logic de tra ve cau tra loi
    # crawl data tu html -> file texts -> tong hop cau tra loi -> dua ra cau dung nhat = AI model sau do gan vao response message
    # dataCanXuLy = 'bla bla'  # can xu dung logic cua AI
    out.cau_tra_loi = fr'{str(x)}'

    return out
