from __future__ import annotations

import logging
import traceback
from typing import Any, Dict

import json

from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.core.config import settings
from src.core.errors.errors import AppError
from src.core.errors.http_code import http
from src.core.errors.messages import msg

logger = logging.getLogger(__name__)

CONTENT_TYPE_PROBLEM_JSON = "application/problem+json"


def _problem_response(status: int, content: Dict[str, Any]) -> Response:
    return Response(
        status_code=status,
        content=json.dumps(content, ensure_ascii=False),
        media_type=CONTENT_TYPE_PROBLEM_JSON,
    )


def register_error_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppError)
    def app_error_handler(request: Request, exc: AppError):
        logger.warning(f"AppError: {exc.title} - {exc.detail}")
        return _problem_response(exc.status, exc.to_dict(instance=request.url.path))

    @app.exception_handler(RequestValidationError)
    def validation_error_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            errors.append({"field": field, "message": error["msg"]})

        logger.warning(f"ValidationError: {errors}")
        return _problem_response(
            http.code.unprocessable_entity,
            {
                "type": "/errors/validation-error",
                "title": "Validation Error",
                "status": http.code.unprocessable_entity,
                "detail": msg.error.validation_error,
                "instance": request.url.path,
                "errors": errors,
            },
        )

    @app.exception_handler(ValidationError)
    def pydantic_validation_error_handler(request: Request, exc: ValidationError):
        errors = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            errors.append({"field": field, "message": error["msg"]})

        logger.warning(f"PydanticValidationError: {errors}")
        return _problem_response(
            http.code.unprocessable_entity,
            {
                "type": "/errors/validation-error",
                "title": "Validation Error",
                "status": http.code.unprocessable_entity,
                "detail": msg.error.validation_error,
                "instance": request.url.path,
                "errors": errors,
            },
        )

    @app.exception_handler(IntegrityError)
    def integrity_error_handler(request: Request, exc: IntegrityError):
        logger.error(f"IntegrityError: {exc.orig}")

        error_msg = str(exc.orig).lower()
        if "unique" in error_msg or "duplicate" in error_msg:
            return _problem_response(
                http.code.conflict,
                {
                    "type": "/errors/conflict",
                    "title": "Conflict",
                    "status": http.code.conflict,
                    "detail": msg.error.conflict,
                    "instance": request.url.path,
                },
            )

        return _build_internal_error_response(request, exc)

    @app.exception_handler(SQLAlchemyError)
    def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"SQLAlchemyError: {exc}", exc_info=True)
        return _build_internal_error_response(request, exc)

    @app.exception_handler(Exception)
    def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(f"UnhandledException: {type(exc).__name__}: {exc}", exc_info=True)
        return _build_internal_error_response(request, exc)


def _build_internal_error_response(request: Request, exc: Exception) -> JSONResponse:
    content: Dict[str, Any] = {
        "type": "/errors/internal-server-error",
        "title": "Internal Server Error",
        "status": http.code.internal_server_error,
        "detail": msg.error.internal_server_error,
        "instance": request.url.path,
    }

    if settings.PROFILE == "dev":
        content["debug"] = {
            "exception": type(exc).__name__,
            "message": str(exc),
            "stacktrace": traceback.format_exc().split("\n"),
        }

    return _problem_response(http.code.internal_server_error, content)
