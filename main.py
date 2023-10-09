
# start sever and get api

from router import query, upload_file, thread_router, history_router
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
from router.exceptions import exceptions


def init_app() -> FastAPI:
    _app = FastAPI(title="CMS API", version="0.2.0")

    _app.include_router(query.ai_router, prefix="/ai", tags=["ai"])
    _app.include_router(upload_file.upload_file_router, prefix="/upload", tags=["upload"])
    # _app.include_router(ai_router.thread_router, prefix="/upload", tags=["upload"])
    # _app.include_router(history_router.history_router, prefix="/save", tags=["save"])
    _app.add_exception_handler(RequestValidationError, exceptions.request_validation_exception_handler)
    _app.add_exception_handler(HTTPException, exceptions.http_exception_handler)

    return _app


app = init_app()

if __name__ == "__main__":
    import uvicorn

    # uvicorn.run("ticket_project.main:app")

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # Set host and port here

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
