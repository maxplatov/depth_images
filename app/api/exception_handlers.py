from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
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
