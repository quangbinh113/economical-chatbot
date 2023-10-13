from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException
import datetime
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, WS_1008_POLICY_VIOLATION
from fastapi.utils import is_body_allowed_for_status_code
from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
import traceback


async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
) -> JSONResponse:
    print("custom default exception handler")
    now = datetime.datetime.now()
    traceback.print_exc()
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": jsonable_encoder(exc.errors()),
                 "time line": now.isoformat()},
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    print("vao day")
    traceback.print_exc()

    return JSONResponse(
        {"detail": exc.detail}, status_code=exc.status_code, headers=headers
    )
