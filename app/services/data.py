from app.models import Launch
from app.services.cache import CacheService
from app.services.spacex_client import SpaceXClient


async def fetch_launches(client: SpaceXClient, cache: CacheService) -> list[Launch]:
    """Fetch all launches with cache-through. Shared by launches and statistics routers."""
    cached = cache.get("/launches")
    if cached is not None:
        return [Launch.model_validate(item) for item in cached]

    launches = await client.get_launches()
    cache.set("/launches", [launch.model_dump(mode="json") for launch in launches])
    return launches
