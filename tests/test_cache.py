from unittest.mock import patch, MagicMock

from src.cache.redis import CacheService


class TestCacheGet:
    def test_returns_none_when_key_missing(self):
        mock_client = MagicMock()
        mock_client.get.return_value = None

        with patch("src.cache.redis.redis.from_url", return_value=mock_client):
            cache = CacheService()
            assert cache.get("missing") is None

        mock_client.get.assert_called_once_with("missing")

    def test_returns_deserialized_dict(self):
        mock_client = MagicMock()
        mock_client.get.return_value = '{"name": "test"}'

        with patch("src.cache.redis.redis.from_url", return_value=mock_client):
            cache = CacheService()
            result = cache.get("key")

        assert result == {"name": "test"}

    def test_returns_deserialized_list(self):
        mock_client = MagicMock()
        mock_client.get.return_value = "[1, 2, 3]"

        with patch("src.cache.redis.redis.from_url", return_value=mock_client):
            cache = CacheService()
            result = cache.get("key")

        assert result == [1, 2, 3]

    def test_returns_plain_string_when_not_json(self):
        mock_client = MagicMock()
        mock_client.get.return_value = "plain text"

        with patch("src.cache.redis.redis.from_url", return_value=mock_client):
            cache = CacheService()
            result = cache.get("key")

        assert result == "plain text"


class TestCacheSet:
    def test_set_without_ttl(self):
        mock_client = MagicMock()

        with patch("src.cache.redis.redis.from_url", return_value=mock_client):
            cache = CacheService()
            cache.set("key", {"data": 123})

        mock_client.set.assert_called_once_with("key", '{"data": 123}')

    def test_set_with_ttl(self):
        mock_client = MagicMock()

        with patch("src.cache.redis.redis.from_url", return_value=mock_client):
            cache = CacheService()
            cache.set("key", {"data": 123}, ttl=300)

        mock_client.setex.assert_called_once_with("key", 300, '{"data": 123}')

    def test_set_plain_string_not_double_serialized(self):
        mock_client = MagicMock()

        with patch("src.cache.redis.redis.from_url", return_value=mock_client):
            cache = CacheService()
            cache.set("key", "simple")

        mock_client.set.assert_called_once_with("key", "simple")


class TestCacheDelete:
    def test_delete_calls_client(self):
        mock_client = MagicMock()

        with patch("src.cache.redis.redis.from_url", return_value=mock_client):
            cache = CacheService()
            cache.delete("key")

        mock_client.delete.assert_called_once_with("key")


class TestCacheExists:
    def test_returns_true_when_key_exists(self):
        mock_client = MagicMock()
        mock_client.exists.return_value = 1

        with patch("src.cache.redis.redis.from_url", return_value=mock_client):
            cache = CacheService()
            assert cache.exists("key") is True

    def test_returns_false_when_key_missing(self):
        mock_client = MagicMock()
        mock_client.exists.return_value = 0

        with patch("src.cache.redis.redis.from_url", return_value=mock_client):
            cache = CacheService()
            assert cache.exists("missing") is False


class TestCacheTtl:
    def test_returns_ttl_value(self):
        mock_client = MagicMock()
        mock_client.ttl.return_value = 245

        with patch("src.cache.redis.redis.from_url", return_value=mock_client):
            cache = CacheService()
            assert cache.ttl("key") == 245

    def test_returns_negative_when_no_ttl(self):
        mock_client = MagicMock()
        mock_client.ttl.return_value = -1

        with patch("src.cache.redis.redis.from_url", return_value=mock_client):
            cache = CacheService()
            assert cache.ttl("key") == -1
