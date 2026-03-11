from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_cache_service, get_spacex_client
from app.models import Launch
from app.services.cache import CacheService
from app.services.spacex_client import SpaceXClient

router = APIRouter(prefix="/launches", tags=["launches"])


async def _fetch_launches(client: SpaceXClient, cache: CacheService) -> list[Launch]:
    """Grab launches from cache or API — shared by list and detail endpoints."""
    cached = cache.get("/launches")
    if cached is not None:
        return [Launch.model_validate(item) for item in cached]

    launches = await client.get_launches()
    # store raw dicts in cache, not pydantic objects
    cache.set("/launches", [l.model_dump(mode="json") for l in launches])
    return launches


def _apply_filters(
    launches: list[Launch],
    *,
    start_date: datetime | None,
    end_date: datetime | None,
    rocket_id: str | None,
    success: bool | None,
    launchpad_id: str | None,
) -> list[Launch]:
    """Filter launches in-memory. Straightforward to test."""
    results = launches

    if start_date:
        results = [l for l in results if l.date_utc >= start_date]
    if end_date:
        results = [l for l in results if l.date_utc <= end_date]
    if rocket_id:
        results = [l for l in results if l.rocket == rocket_id]
    if success is not None:
        results = [l for l in results if l.success is success]
    if launchpad_id:
        results = [l for l in results if l.launchpad == launchpad_id]

    return results


@router.get("", response_model=list[Launch])
async def list_launches(
    client: SpaceXClient = Depends(get_spacex_client),
    cache: CacheService = Depends(get_cache_service),
    start_date: datetime | None = Query(None, description="Filter launches after this date (ISO 8601)"),
    end_date: datetime | None = Query(None, description="Filter launches before this date (ISO 8601)"),
    rocket_id: str | None = Query(None, description="Filter by rocket UUID"),
    success: bool | None = Query(None, description="Filter by launch success"),
    launchpad_id: str | None = Query(None, description="Filter by launchpad UUID"),
):
    launches = await _fetch_launches(client, cache)
    return _apply_filters(
        launches,
        start_date=start_date,
        end_date=end_date,
        rocket_id=rocket_id,
        success=success,
        launchpad_id=launchpad_id,
    )


@router.get("/{launch_id}", response_model=Launch)
async def get_launch(
    launch_id: str,
    client: SpaceXClient = Depends(get_spacex_client),
    cache: CacheService = Depends(get_cache_service),
):
    # try to find it in the cached list first before hitting the API
    cached = cache.get("/launches")
    if cached is not None:
        for item in cached:
            if item.get("id") == launch_id:
                return Launch.model_validate(item)

    return await client.get_launch(launch_id)