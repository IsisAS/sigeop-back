from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from tests.helpers import (
    StatusFactory,
    assert_problem_json,
    assert_not_found,
    assert_validation_error,
    assert_internal_error,
)
from src.core.errors.errors import (
    AppError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    ValidationError,
    InternalServerError,
)
from src.modules.pedido.status.status_schema import StatusReadDTO

STATUS_URL = StatusFactory.URL


class TestRFC7807Format:
    """Valida estrutura RFC 7807 em todas as respostas de erro."""

    def test_content_type_is_problem_json(self, client: TestClient):
        with patch(
            "src.modules.pedido.status.status_service.StatusService.list",
            side_effect=NotFoundError("not found"),
        ):
            response = client.get(STATUS_URL)
            assert response.headers["content-type"] == "application/problem+json"

    def test_not_found_format(self, client: TestClient):
        with patch(
            "src.modules.pedido.status.status_service.StatusService.list",
            side_effect=NotFoundError("not found"),
        ):
            response = client.get(STATUS_URL)
            data = assert_not_found(response)
            assert data["instance"] == STATUS_URL

    def test_validation_format(self, client: TestClient):
        def raise_pydantic_error(*args, **kwargs):
            StatusReadDTO.model_validate({"invalid": "data"})

        with patch(
            "src.modules.pedido.status.status_service.StatusService.list",
            side_effect=raise_pydantic_error,
        ):
            response = client.get(STATUS_URL)
            data = assert_validation_error(response)
            assert data["instance"] == STATUS_URL

    def test_conflict_format(self, client: TestClient):
        with patch(
            "src.modules.pedido.status.status_service.StatusService.list",
            side_effect=IntegrityError("", {}, Exception("UNIQUE constraint failed")),
        ):
            response = client.get(STATUS_URL)
            assert_problem_json(response, status=409, error_type="/errors/conflict")


class TestAppErrors:
    """Testa todas as subclasses de AppError."""

    def test_app_error_default(self):
        err = AppError()
        assert err.detail == "Requisição inválida."
        assert err.status == 400

    def test_app_error_custom_detail(self):
        err = AppError("Algo deu errado")
        assert err.detail == "Algo deu errado"

    def test_app_error_with_extra(self):
        err = AppError("Erro", extra={"retry_after": 30})
        data = err.to_dict(instance="/test")
        assert data["instance"] == "/test"
        assert data["retry_after"] == 30

    def test_app_error_to_dict_without_instance(self):
        err = AppError("Erro")
        data = err.to_dict()
        assert "instance" not in data

    def test_bad_request_error(self):
        err = BadRequestError()
        assert err.type == "/errors/bad-request"
        assert err.status == 400

    def test_unauthorized_error(self):
        err = UnauthorizedError()
        assert err.type == "/errors/unauthorized"
        assert err.status == 401

    def test_forbidden_error(self):
        err = ForbiddenError()
        assert err.type == "/errors/forbidden"
        assert err.status == 403

    def test_not_found_error(self):
        err = NotFoundError()
        assert err.type == "/errors/not-found"
        assert err.status == 404

    def test_conflict_error(self):
        err = ConflictError()
        assert err.type == "/errors/conflict"
        assert err.status == 409

    def test_validation_error(self):
        err = ValidationError()
        assert err.type == "/errors/validation-error"
        assert err.status == 422

    def test_internal_server_error(self):
        err = InternalServerError()
        assert err.type == "/errors/internal-server-error"
        assert err.status == 500


class TestHandlerPydanticValidationError:
    """Testa o handler de ValidationError do Pydantic."""

    def test_pydantic_validation_error_returns_422(self, client: TestClient):
        def raise_pydantic_error(*args, **kwargs):
            StatusReadDTO.model_validate({"invalid": "data"})

        with patch(
            "src.modules.pedido.status.status_service.StatusService.list",
            side_effect=raise_pydantic_error,
        ):
            response = client.get(STATUS_URL)
            assert_validation_error(response)


class TestHandlerIntegrityError:
    """Testa o handler de IntegrityError (unique constraint e genérico)."""

    def test_unique_violation_returns_conflict(self, client: TestClient):
        with patch(
            "src.modules.pedido.status.status_service.StatusService.list",
            side_effect=IntegrityError("", {}, Exception("UNIQUE constraint failed")),
        ):
            response = client.get(STATUS_URL)
            assert_problem_json(response, status=409, error_type="/errors/conflict")

    def test_generic_integrity_error_returns_500(self, client: TestClient):
        with patch(
            "src.modules.pedido.status.status_service.StatusService.list",
            side_effect=IntegrityError("", {}, Exception("some other constraint")),
        ):
            response = client.get(STATUS_URL)
            assert_internal_error(response)


class TestHandlerSQLAlchemyError:
    """Testa o handler de SQLAlchemyError genérico."""

    def test_sqlalchemy_error_returns_500(self, client: TestClient):
        with patch(
            "src.modules.pedido.status.status_service.StatusService.list",
            side_effect=SQLAlchemyError("connection lost"),
        ):
            response = client.get(STATUS_URL)
            assert_internal_error(response)


class TestHandlerUnhandledException:
    """Testa o handler de exceções não previstas."""

    def test_unhandled_exception_returns_500(self, client: TestClient):
        with patch(
            "src.modules.pedido.status.status_service.StatusService.list",
            side_effect=RuntimeError("unexpected boom"),
        ):
            response = client.get(STATUS_URL)
            data = assert_internal_error(response)
            assert data["debug"]["exception"] == "RuntimeError"

    def test_unhandled_exception_hides_debug_in_prod(self, client: TestClient):
        with (
            patch("src.core.errors.handlers.settings") as mock_settings,
            patch(
                "src.modules.pedido.status.status_service.StatusService.list",
                side_effect=RuntimeError("boom"),
            ),
        ):
            mock_settings.ENV = "prod"
            response = client.get(STATUS_URL)
            data = response.json()
            assert data["status"] == 500
            assert "debug" not in data
