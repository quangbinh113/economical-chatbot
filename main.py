# from src.model.model import HandleQA
# from config.config import config
# import os 
# from src.getdata.user_query import get_data
# # path = r'C:\Users\anh.do\Desktop\chatbot\data\data'
# path = 'data/data'
# # query = 'Tình hình đại hội cổ đông ngân hàng Techcombank?'
# # query = 'Nhận định về xu hướng cổ phiếu TCB tháng tới?'
# query = 'Xu hướng giá Bitcoin trong thời gian tới'
# # query = ''

# get_data(query,query_folder = path)
# files = os.listdir(path)
# files = [os.path.join(path,file) for file in files]
# chat = HandleQA(config)

# x = chat.ask_gpt(query,files)
# print(x)


# start sever and get api

from router import query,upload_file
from fastapi import FastAPI
def init_app() -> FastAPI:


    _app = FastAPI(title="CMS API", version="0.2.0")

    _app.include_router(query.ai_router, prefix="/ai", tags=["ai"])
    _app.include_router(upload_file.upload_file_router, prefix="/upload", tags=["upload"])

    
    return _app


app = init_app()


if __name__ == "__main__":
    import uvicorn
    # uvicorn.run("ticket_project.main:app")

    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)  # Set host and port here


# from fastapi import FastAPI
# from pydantic import BaseModel
# from src.database import engine
# from src.schemas import Chat
# from src.model.model import HandleQA
# from config.config import config
# from dotenv import load_dotenv,find_dotenv
# from src.get_data.user_query import get_data
# _ = load_dotenv(find_dotenv())
# import os 
# app = FastAPI()

# bot = HandleQA(config)

# @app.get('/')
# def hello_world():
#     return {
#         'res':'hello world'
#     }


# @app.post("/chat")
# def chat(req:Chat):
#     path = r'C:\Users\anh.do\Desktop\chatbot\data\drive-download-20230920T080751Z-001\data'
#     get_data(req.question,query_folder = path)

#     files = os.listdir(path)
#     files = [os.path.join(path,file) for file in files]

#     answer = bot.ask_gpt(req.question,files)
#     return {'answer':answer}