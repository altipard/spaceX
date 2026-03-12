from pathlib import Path

import pytest

from app.config import Settings
from app.services.cache import CacheService


@pytest.fixture
def cache(tmp_path: Path) -> CacheService:
    """Create a CacheService backed by a temp directory — no leftover .db files."""
    settings = Settings(cache_dir=tmp_path, cache_ttl=60)
    return CacheService(settings)


def test_get_returns_none_on_miss(cache: CacheService):
    assert cache.get("/launches") is None


def test_set_then_get(cache: CacheService):
    data = [{"id": "1", "name": "test"}]
    cache.set("/launches", data)
    assert cache.get("/launches") == data


def test_different_keys_are_independent(cache: CacheService):
    cache.set("/launches", [{"a": 1}])
    cache.set("/rockets", [{"b": 2}])
    assert cache.get("/launches") == [{"a": 1}]
    assert cache.get("/rockets") == [{"b": 2}]


def test_set_overwrites_existing(cache: CacheService):
    cache.set("/launches", [{"v": 1}])
    cache.set("/launches", [{"v": 2}])
    assert cache.get("/launches") == [{"v": 2}]


def test_expired_entry_returns_none(tmp_path: Path):
    settings = Settings(cache_dir=tmp_path, cache_ttl=0)  # ttl=0 → always expired
    cache = CacheService(settings)
    cache.set("/launches", [{"id": "1"}])
    assert cache.get("/launches") is None


def test_clear_removes_all_entries(cache: CacheService):
    cache.set("/launches", [{"a": 1}])
    cache.set("/rockets", [{"b": 2}])
    cache.clear()
    assert cache.get("/launches") is None
    assert cache.get("/rockets") is None
