import logging

import alembic.config
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette._exception_handler import ExceptionHandlers
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
)
from app.api.middlewares import add_process_time_header
from app.api.routers.images import images_router
from app.db.engine import DatabaseManager
from app.models.base import HTTPErrorModel
from app.repository.images import ImagesRepository
from app.service.images import ImagesService
from app.settings import Settings

logger = logging.getLogger(__name__)


def setup_routes(app: FastAPI) -> None:
    app.include_router(images_router, prefix="/api/v1", tags=["images"])


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def get_exception_handlers() -> ExceptionHandlers:
    return {
        StarletteHTTPException: http_exception_handler,
        RequestValidationError: validation_exception_handler,
    }


def run_migrations() -> None:
    conf = alembic.config.Config("alembic.ini")
    conf.attributes["configure_logger"] = False
    alembic.command.upgrade(conf, "head")


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title="Depth images",
        exception_handlers=get_exception_handlers(),
        responses={422: {"model": HTTPErrorModel}},
    )
    setup_routes(app)
    run_migrations()
    setup_middlewares(app)

    @app.on_event("startup")
    def on_startup():
        db_manager = DatabaseManager(settings.db)
        image_repository = ImagesRepository(db_manager)

        app.state.image_service = ImagesService(image_repository)
        logger.info("On startup end")

    return app
