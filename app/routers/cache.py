from fastapi import APIRouter, Depends

from app.dependencies import get_cache_service
from app.services.cache import CacheService

router = APIRouter(prefix="/cache", tags=["cache"])


@router.delete("")
async def clear_cache(cache: CacheService = Depends(get_cache_service)):
    """Drop all cached data. then the API call will fetch fresh data from SpaceX."""
    cache.clear()
    return {"message": "cache cleared"}
