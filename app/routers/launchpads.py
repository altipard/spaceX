from fastapi import APIRouter, Depends

from app.dependencies import get_cache_service, get_spacex_client
from app.models import Launchpad
from app.services.cache import CacheService
from app.services.spacex_client import SpaceXClient

router = APIRouter(prefix="/launchpads", tags=["launchpads"])


@router.get("", response_model=list[Launchpad])
async def list_launchpads(
    client: SpaceXClient = Depends(get_spacex_client),
    cache: CacheService = Depends(get_cache_service),
):
    cached = cache.get("/launchpads")
    if cached is not None:
        return [Launchpad.model_validate(item) for item in cached]

    launchpads = await client.get_launchpads()
    cache.set("/launchpads", [lp.model_dump(mode="json") for lp in launchpads])
    return launchpads


@router.get("/{launchpad_id}", response_model=Launchpad)
async def get_launchpad(
    launchpad_id: str,
    client: SpaceXClient = Depends(get_spacex_client),
    cache: CacheService = Depends(get_cache_service),
):
    cached = cache.get("/launchpads")
    if cached is not None:
        for item in cached:
            if item.get("id") == launchpad_id:
                return Launchpad.model_validate(item)

    return await client.get_launchpad(launchpad_id)