from fastapi import APIRouter, Body, Depends, Response, status, Request, Query, UploadFile, File

from flask import Flask, request, send_file
from starlette.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from src.model.model import HandleQA
from config.config import config
import os 
from src.getdata.user_query import get_data

ai_router = APIRouter()



class AIResponseModel(BaseModel):
    cau_tra_loi: Optional[str]


class AIQueryModel(BaseModel):
    question: str


@ai_router.post('/get_response')
async def get_response(input_: AIQueryModel):
    path = 'data/data'
    questionUser = input_.question
    out = AIResponseModel(cau_tra_loi=None)
    # if input_.question == 'gia co phieu ngay hom nay':
    #     out.cau_tra_loi = 'may deo mua duoc dau'
    #     return out
    dataCanXuLy = ""

    get_data(questionUser,query_folder = path)
    files = os.listdir(path)
    files = [os.path.join(path,file) for file in files]
    chat = HandleQA(config)

    x = chat.ask_gpt(questionUser,files)

    # code logic de tra ve cau tra loi
    # crawl data tu html -> file texts -> tong hop cau tra loi -> dua ra cau dung nhat = AI model sau do gan vao response message
    # dataCanXuLy = 'bla bla'  # can xu dung logic cua AI
    out.cau_tra_loi = fr'cau tra loi cua {questionUser} la {str(x)}'

    return out
