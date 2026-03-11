# dependency factories for FastAPI's Depends() injection.
# never done this in python before :-)
# routers import these — never instantiate services directly.


from app.config import Settings, get_settings
from app.services.cache import CacheService
from app.services.spacex_client import SpaceXClient


def get_settings_dep() -> Settings:
    return get_settings()


def get_spacex_client() -> SpaceXClient:
    return SpaceXClient(get_settings())


def get_cache_service() -> CacheService:
    return CacheService(get_settings())