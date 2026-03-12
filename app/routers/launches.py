import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from app.dependencies import get_cache_service, get_spacex_client
from app.models import Launch
from app.services.cache import CacheService
from app.services.data import fetch_launches
from app.services.spacex_client import SpaceXClient

router = APIRouter(prefix="/launches", tags=["launches"])


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
        results = [launch for launch in results if launch.date_utc >= start_date]
    if end_date:
        results = [launch for launch in results if launch.date_utc <= end_date]
    if rocket_id:
        results = [launch for launch in results if launch.rocket == rocket_id]
    if success is not None:
        results = [launch for launch in results if launch.success is success]
    if launchpad_id:
        results = [launch for launch in results if launch.launchpad == launchpad_id]

    return results


def _launches_to_csv(launches: list[Launch]) -> str:
    """Serialize launches to a CSV string."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "name", "flight_number", "date_utc", "rocket", "launchpad", "success"])

    for launch in launches:
        writer.writerow(
            [
                launch.id,
                launch.name,
                launch.flight_number,
                launch.date_utc.isoformat(),
                launch.rocket,
                launch.launchpad,
                launch.success,
            ]
        )

    return buf.getvalue()


@router.get("")
async def list_launches(
    client: SpaceXClient = Depends(get_spacex_client),
    cache: CacheService = Depends(get_cache_service),
    start_date: datetime | None = Query(None, description="Filter launches after this date (ISO 8601)"),
    end_date: datetime | None = Query(None, description="Filter launches before this date (ISO 8601)"),
    rocket_id: str | None = Query(None, description="Filter by rocket UUID"),
    success: bool | None = Query(None, description="Filter by launch success"),
    launchpad_id: str | None = Query(None, description="Filter by launchpad UUID"),
    export: str | None = Query(None, description="Export format: 'csv' for CSV download, omit for JSON"),
    refresh: bool = Query(False, description="bypass cache and fetch fresh data from SpaceX API"),
):
    if refresh:
        launches = await client.get_launches()
        cache.set("/launches", [launch.model_dump(mode="json") for launch in launches])
    else:
        launches = await fetch_launches(client, cache)

    filtered = _apply_filters(
        launches,
        start_date=start_date,
        end_date=end_date,
        rocket_id=rocket_id,
        success=success,
        launchpad_id=launchpad_id,
    )

    if export == "csv":
        content = _launches_to_csv(filtered)
        return StreamingResponse(
            iter([content]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=launches.csv"},
        )

    return filtered


@router.get("/{launch_id}", response_model=Launch)
async def get_launch(
    launch_id: str,
    client: SpaceXClient = Depends(get_spacex_client),
    cache: CacheService = Depends(get_cache_service),
):
    cached = cache.get("/launches")
    if cached is not None:
        for item in cached:
            if item.get("id") == launch_id:
                return Launch.model_validate(item)

    return await client.get_launch(launch_id)
