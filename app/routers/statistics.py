from fastapi import APIRouter, Depends

from app.dependencies import get_cache_service, get_spacex_client
from app.models import Launchpad, Rocket
from app.services import statistics as stats
from app.services.cache import CacheService
from app.services.data import fetch_launches
from app.services.spacex_client import SpaceXClient

router = APIRouter(prefix="/statistics", tags=["statistics"])


async def _get_rockets_map(client: SpaceXClient, cache: CacheService) -> dict[str, str]:
    """Build a {uuid: name} lookup for rockets."""
    cached = cache.get("/rockets")
    if cached is not None:
        rockets = [Rocket.model_validate(item) for item in cached]
    else:
        rockets = await client.get_rockets()
        cache.set("/rockets", [r.model_dump(mode="json") for r in rockets])

    return {r.id: r.name for r in rockets}


async def _get_launchpads_map(client: SpaceXClient, cache: CacheService) -> dict[str, str]:
    """Build a {uuid: name} lookup for launchpads."""
    cached = cache.get("/launchpads")
    if cached is not None:
        launchpads = [Launchpad.model_validate(item) for item in cached]
    else:
        launchpads = await client.get_launchpads()
        cache.set("/launchpads", [lp.model_dump(mode="json") for lp in launchpads])

    return {lp.id: lp.name for lp in launchpads}


@router.get("/success-rate")
async def get_success_rate(
    client: SpaceXClient = Depends(get_spacex_client),
    cache: CacheService = Depends(get_cache_service),
):
    launches = await fetch_launches(client, cache)
    rockets_map = await _get_rockets_map(client, cache)
    return stats.success_rate_by_rocket(launches, rockets_map)


@router.get("/launches-per-site")
async def get_launches_per_site(
    client: SpaceXClient = Depends(get_spacex_client),
    cache: CacheService = Depends(get_cache_service),
):
    launches = await fetch_launches(client, cache)
    launchpads_map = await _get_launchpads_map(client, cache)
    return stats.launches_per_site(launches, launchpads_map)


@router.get("/launch-frequency")
async def get_launch_frequency(
    client: SpaceXClient = Depends(get_spacex_client),
    cache: CacheService = Depends(get_cache_service),
):
    launches = await fetch_launches(client, cache)
    return stats.launch_frequency(launches)