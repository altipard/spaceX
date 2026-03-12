import httpx

from app.config import Settings
from app.exceptions import ResourceNotFoundError, SpaceXAPIError
from app.models import Launch, Launchpad, Rocket


class SpaceXClient:
    """Thin wrapper around the SpaceX v4 REST API."""

    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.spacex_base_url

    async def _get(self, path: str) -> list[dict] | dict:
        """Fire a GET request and return parsed JSON.

        Raises SpaceXAPIError on any network or HTTP error so the
        caller never has to deal with raw httpx exceptions.
        """
        url = f"{self._base_url}{path}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            raise SpaceXAPIError(f"SpaceX API returned {exc.response.status_code} for {path}") from exc
        except httpx.RequestError as exc:
            raise SpaceXAPIError(f"Could not reach SpaceX API: {exc}") from exc


    async def get_launches(self) -> list[Launch]:
        data = await self._get("/launches")
        return [Launch.model_validate(item) for item in data]

    async def get_launch(self, launch_id: str) -> Launch:
        try:
            data = await self._get(f"/launches/{launch_id}")
        except SpaceXAPIError as exc:
            if "404" in exc.detail:
                raise ResourceNotFoundError("launch", launch_id) from exc
            raise
        return Launch.model_validate(data)

    async def get_rockets(self) -> list[Rocket]:
        data = await self._get("/rockets")
        return [Rocket.model_validate(item) for item in data]

    async def get_rocket(self, rocket_id: str) -> Rocket:
        try:
            data = await self._get(f"/rockets/{rocket_id}")
        except SpaceXAPIError as exc:
            if "404" in exc.detail:
                raise ResourceNotFoundError("rocket", rocket_id) from exc
            raise
        return Rocket.model_validate(data)

    async def get_launchpads(self) -> list[Launchpad]:
        data = await self._get("/launchpads")
        return [Launchpad.model_validate(item) for item in data]

    async def get_launchpad(self, launchpad_id: str) -> Launchpad:
        try:
            data = await self._get(f"/launchpads/{launchpad_id}")
        except SpaceXAPIError as exc:
            if "404" in exc.detail:
                raise ResourceNotFoundError("launchpad", launchpad_id) from exc
            raise
        return Launchpad.model_validate(data)
