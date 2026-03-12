from fastapi import APIRouter, Depends

from app.dependencies import get_cache_service, get_spacex_client
from app.models import Rocket
from app.services.cache import CacheService
from app.services.spacex_client import SpaceXClient

router = APIRouter(prefix="/rockets", tags=["rockets"])


@router.get("", response_model=list[Rocket])
async def list_rockets(
    client: SpaceXClient = Depends(get_spacex_client),
    cache: CacheService = Depends(get_cache_service),
):
    cached = cache.get("/rockets")
    if cached is not None:
        return [Rocket.model_validate(item) for item in cached]

    rockets = await client.get_rockets()
    cache.set("/rockets", [r.model_dump(mode="json") for r in rockets])
    return rockets


@router.get("/{rocket_id}", response_model=Rocket)
async def get_rocket(
    rocket_id: str,
    client: SpaceXClient = Depends(get_spacex_client),
    cache: CacheService = Depends(get_cache_service),
):
    cached = cache.get("/rockets")
    if cached is not None:
        for item in cached:
            if item.get("id") == rocket_id:
                return Rocket.model_validate(item)

    return await client.get_rocket(rocket_id)