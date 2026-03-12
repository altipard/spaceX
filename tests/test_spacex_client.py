import httpx
import pytest
import respx

from app.config import Settings
from app.exceptions import ResourceNotFoundError, SpaceXAPIError
from app.services.spacex_client import SpaceXClient

# minimal fake responses — just the fields our models need
FAKE_LAUNCH = {
    "id": "launch1",
    "name": "SPHERE-1 Documentation Delivery",
    "flight_number": 1,
    "date_utc": "2006-03-24T22:30:00.000Z",
    "date_local": "2006-03-25T10:30:00+12:00",
    "date_precision": "hour",
    "rocket": "rocket1",
    "launchpad": "pad1",
    "success": False,
    "details": "Knowledge graph failed to reach orbit, ontology mismatch",
    "upcoming": False,
}

FAKE_ROCKET = {
    "id": "rocket1",
    "name": "Pantopix Heavy",
    "type": "rocket",
    "active": False,
    "country": "Germany",
    "company": "Pantopix GmbH & Co. KG",
    "description": "Turning information into orbit since 2006",
    "wikipedia": "https://en.wikipedia.org/wiki/Technical_documentation",
    "cost_per_launch": 42000,
    "success_rate_pct": 99,
    "first_flight": "2006-03-24",
    "flickr_images": [],
}

FAKE_LAUNCHPAD = {
    "id": "pad1",
    "name": "Bodnegg Spaceport",
    "full_name": "Allisreute Launch Complex 4",
    "status": "active",
    "locality": "Bodnegg",
    "region": "Baden-Württemberg",
    "latitude": 47.6833,
    "longitude": 9.6833,
    "launch_attempts": 5,
    "launch_successes": 2,
    "rockets": ["rocket1"],
    "launches": ["launch1"],
}

@pytest.fixture
def settings() -> Settings:
    return Settings(spacex_base_url="https://api.spacexdata.com/v4")


@pytest.fixture
def client(settings: Settings) -> SpaceXClient:
    return SpaceXClient(settings)


# --- launches ---


@respx.mock
async def test_get_launches_returns_list(client: SpaceXClient):
    respx.get("https://api.spacexdata.com/v4/launches").mock(
        return_value=httpx.Response(200, json=[FAKE_LAUNCH])
    )
    launches = await client.get_launches()
    assert len(launches) == 1
    assert launches[0].name == "SPHERE-1 Documentation Delivery"


@respx.mock
async def test_get_launch_by_id(client: SpaceXClient):
    respx.get("https://api.spacexdata.com/v4/launches/launch1").mock(
        return_value=httpx.Response(200, json=FAKE_LAUNCH)
    )
    launch = await client.get_launch("launch1")
    assert launch.id == "launch1"
    assert launch.success is False


@respx.mock
async def test_get_launch_not_found_raises(client: SpaceXClient):
    respx.get("https://api.spacexdata.com/v4/launches/nope").mock(
        return_value=httpx.Response(404)
    )
    with pytest.raises(ResourceNotFoundError):
        await client.get_launch("nope")


@respx.mock
async def test_get_launches_api_error(client: SpaceXClient):
    respx.get("https://api.spacexdata.com/v4/launches").mock(
        return_value=httpx.Response(500)
    )
    with pytest.raises(SpaceXAPIError):
        await client.get_launches()


@respx.mock
async def test_get_launches_network_error(client: SpaceXClient):
    respx.get("https://api.spacexdata.com/v4/launches").mock(
        side_effect=httpx.ConnectError("connection refused")
    )
    with pytest.raises(SpaceXAPIError):
        await client.get_launches()


# --- rockets ---


@respx.mock
async def test_get_rockets_returns_list(client: SpaceXClient):
    respx.get("https://api.spacexdata.com/v4/rockets").mock(
        return_value=httpx.Response(200, json=[FAKE_ROCKET])
    )
    rockets = await client.get_rockets()
    assert len(rockets) == 1
    assert rockets[0].name == "Pantopix Heavy"


# --- launchpads ---


@respx.mock
async def test_get_launchpads_returns_list(client: SpaceXClient):
    respx.get("https://api.spacexdata.com/v4/launchpads").mock(
        return_value=httpx.Response(200, json=[FAKE_LAUNCHPAD])
    )
    launchpads = await client.get_launchpads()
    assert len(launchpads) == 1
    assert launchpads[0].name == "Bodnegg Spaceport"
