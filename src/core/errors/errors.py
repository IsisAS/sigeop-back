from __future__ import annotations

from typing import Optional, Dict, Any

from src.core.errors.http_code import http
from src.core.errors.messages import msg


class AppError(Exception):
    """
    Exceção base da aplicação seguindo RFC 7807 (Problem Details).

    Formato:
      - type: URI identificando o tipo de erro
      - title: título curto e legível
      - status: código HTTP
      - detail: descrição detalhada
      - instance: URI da requisição (adicionado pelo handler)
    """
    TYPE: str = "about:blank"
    TITLE: str = "App Error"
    STATUS: int = http.code.bad_request
    DEFAULT_DETAIL: str = msg.error.bad_request

    def __init__(self, detail: Optional[str] = None, *, extra: Optional[Dict[str, Any]] = None):
        self.type = self.TYPE
        self.title = self.TITLE
        self.status = self.STATUS
        self.detail = detail or self.DEFAULT_DETAIL
        self.extra = extra or {}
        super().__init__(self.detail)

    def to_dict(self, instance: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "type": self.type,
            "title": self.title,
            "status": self.status,
            "detail": self.detail,
        }
        if instance:
            payload["instance"] = instance
        if self.extra:
            payload.update(self.extra)
        return payload


class BadRequestError(AppError):
    TYPE = "/errors/bad-request"
    TITLE = "Bad Request"
    STATUS = http.code.bad_request
    DEFAULT_DETAIL = msg.error.bad_request


class UnauthorizedError(AppError):
    TYPE = "/errors/unauthorized"
    TITLE = "Unauthorized"
    STATUS = http.code.unauthorized
    DEFAULT_DETAIL = msg.error.unauthorized


class ForbiddenError(AppError):
    TYPE = "/errors/forbidden"
    TITLE = "Forbidden"
    STATUS = http.code.forbidden
    DEFAULT_DETAIL = msg.error.forbidden


class NotFoundError(AppError):
    TYPE = "/errors/not-found"
    TITLE = "Not Found"
    STATUS = http.code.not_found
    DEFAULT_DETAIL = msg.error.not_found


class ConflictError(AppError):
    TYPE = "/errors/conflict"
    TITLE = "Conflict"
    STATUS = http.code.conflict
    DEFAULT_DETAIL = msg.error.conflict


class ValidationError(AppError):
    TYPE = "/errors/validation-error"
    TITLE = "Validation Error"
    STATUS = http.code.unprocessable_entity
    DEFAULT_DETAIL = msg.error.validation_error


class InternalServerError(AppError):
    TYPE = "/errors/internal-server-error"
    TITLE = "Internal Server Error"
    STATUS = http.code.internal_server_error
    DEFAULT_DETAIL = msg.error.internal_server_error
