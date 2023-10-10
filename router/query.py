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

ai_router = APIRouter()
chat = HandleQA(config)

class AIResponseModel(BaseModel):
    cau_tra_loi: Optional[str]


class AIQueryModel(BaseModel):
    question: str
    documents: str | None = None


@ai_router.post('/get_response')
async def get_response(input_: AIQueryModel):
    # path = 'data/data'
    # chat = HandleQA(config)
    questionUser = input_.question
    out = AIResponseModel(cau_tra_loi=None)
    if input_.documents:
        generator = chat.ask_gpt(questionUser,documents = input_.documents)
    else:     
    # x = chat.ask_gpt(questionUser,crawl_data=crawl_data)
    
    # code logic de tra ve cau tra loi
    # crawl data tu html -> file texts -> tong hop cau tra loi -> dua ra cau dung nhat = AI model sau do gan vao response message
    # dataCanXuLy = 'bla bla'  # can xu dung logic cua AI

    # if not generator:
     #     return
        crawl_data = get_data(questionUser) 
        generator = chat.ask_gpt(questionUser,crawl_data=crawl_data,documents = None)
    print(generator)
    return StreamingResponse(generator, media_type="text/event-stream")
    
    # out.cau_tra_loi = fr'{str(x)}'

    # return out