# Dependency factories for FastAPI's Depends() injection.
#
# HOW THIS WORKS:
# 1. Services (CacheService, SpaceXClient) are created ONCE in main.py's lifespan
#    and stored on app.state — that's the singleton.
# 2. These functions below just return the already-created instance from app.state.
#    FastAPI calls them on every request, but they're cheap — just attribute access.
# 3. Routes declare dependencies like: cache: CacheService = Depends(get_cache_service)
#    and FastAPI auto-injects the Request object into these functions for us.
#
# WHY NOT just import the service directly in routes?
# Because Depends() makes testing easy — you can swap any dep with:
#   app.dependency_overrides[get_cache_service] = lambda: my_mock_cache

from fastapi import Request

from app.config import Settings, get_settings
from app.services.cache import CacheService
from app.services.spacex_client import SpaceXClient


def get_settings_dep() -> Settings:
    return get_settings()


def get_spacex_client(request: Request) -> SpaceXClient:
    return request.app.state.spacex_client


def get_cache_service(request: Request) -> CacheService:
    return request.app.state.cache
