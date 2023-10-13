# start sever and get api
from router.exceptions import exceptions
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException
from router import query, upload_file
import sys
import uvicorn

sys.path.append(__file__)


def init_app() -> FastAPI:
    _app = FastAPI(title="CMS API", version="0.2.0")
    _app.include_router(query.ai_router, prefix="/ai", tags=["ai"])
    _app.include_router(upload_file.upload_file_router,
                        prefix="/upload", tags=["upload"])
    _app.add_exception_handler(
        RequestValidationError, exceptions.request_validation_exception_handler)
    _app.add_exception_handler(
        HTTPException, exceptions.http_exception_handler)
    return _app

app = init_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                reload=True)  # Set host and port here