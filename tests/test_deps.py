from unittest.mock import patch, MagicMock

from src.cache.redis import CacheService
from src.core.deps import get_db, get_cache


class TestGetDb:
    def test_yields_session_and_closes(self):
        mock_session = MagicMock()
        mock_session_local = MagicMock(return_value=mock_session)

        with patch("src.core.deps.SessionLocal", mock_session_local):
            gen = get_db()
            db = next(gen)
            assert db == mock_session

            try:
                next(gen)
            except StopIteration:
                pass

            mock_session.close.assert_called_once()

    def test_closes_session_on_exception(self):
        mock_session = MagicMock()
        mock_session_local = MagicMock(return_value=mock_session)

        with patch("src.core.deps.SessionLocal", mock_session_local):
            gen = get_db()
            next(gen)

            try:
                gen.throw(RuntimeError("boom"))
            except RuntimeError:
                pass

            mock_session.close.assert_called_once()


class TestGetCache:
    def test_returns_cache_service_instance(self):
        with patch("src.core.deps.CacheService") as MockCacheService:
            result = get_cache()
            MockCacheService.assert_called_once()
            assert result == MockCacheService.return_value
