import sys

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.models.base import HTTPErrorModel


async def http_exception_handler(
    _: Request, exception_: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exception_.status_code,
        content=HTTPErrorModel(
            message=exception_.detail, status_code=exception_.status_code
        ).model_dump(),
    )


async def validation_exception_handler(
    _: Request,
    exception_: RequestValidationError,
) -> JSONResponse:
    message = "; ".join(
        [
            f"Field {'.'.join(str(e) for e in error['loc'])}: {error['msg']}"
            for error in exception_.errors()
        ]
    )
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=HTTPErrorModel(
            message=message, status_code=HTTP_422_UNPROCESSABLE_ENTITY
        ).model_dump(),
    )


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> PlainTextResponse:
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )
    exception_type, exception_value, _ = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    logger.error(
        f'{host}:{port} - "{request.method} {url}" '
        f"500 Internal Server Error <{exception_name}: {exception_value}>"
    )
    return PlainTextResponse(
        f"Something went wrong. Exception: {exc}", status_code=500
    )
