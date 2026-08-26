from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from redis.exceptions import ConnectionError

from src.cache.redis import CacheService
from src.core.config import settings
from src.core.deps import get_cache
from src.main import app

REDIS_HEALTH_URL = f"{settings.PREFIX_ROUTER}/health/redis"
CICLO_HEALTH_URL = f"{settings.PREFIX_ROUTER}/health/ciclo"


def _mock_cache(mock_client: MagicMock):
    """Cria override de get_cache com client mockado."""
    cache = CacheService.__new__(CacheService)
    cache.client = mock_client

    def override():
        return cache

    return override


class TestRedisHealthy:
    def test_returns_healthy_when_ping_succeeds(self):
        mock_client = MagicMock()
        mock_client.ping.return_value = True

        app.dependency_overrides[get_cache] = _mock_cache(mock_client)
        with TestClient(app) as client:
            response = client.get(REDIS_HEALTH_URL)

        app.dependency_overrides.clear()

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "redis"
        assert "detail" not in data


class TestRedisUnhealthy:
    def test_returns_unhealthy_when_ping_fails(self):
        mock_client = MagicMock()
        mock_client.ping.side_effect = ConnectionError("Connection refused")

        app.dependency_overrides[get_cache] = _mock_cache(mock_client)
        with TestClient(app) as client:
            response = client.get(REDIS_HEALTH_URL)

        app.dependency_overrides.clear()

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["service"] == "redis"
        assert "Connection refused" in data["detail"]


class TestCicloHealthy:
    @patch("src.modules.health.health_router.CicloClient")
    def test_returns_healthy_when_ciclo_is_ok(self, mock_cls):
        mock_cls.return_value.health_check.return_value = True

        with TestClient(app) as client:
            response = client.get(CICLO_HEALTH_URL)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "ciclo"


class TestCicloUnhealthy:
    @patch("src.modules.health.health_router.CicloClient")
    def test_returns_unhealthy_when_ciclo_fails(self, mock_cls):
        mock_cls.return_value.health_check.return_value = False

        with TestClient(app) as client:
            response = client.get(CICLO_HEALTH_URL)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["service"] == "ciclo"
