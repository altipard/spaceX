# the services will raise those exceptions — routers never catch them manually.


class SpaceXAPIError(Exception):
    """SpaceX v4 API is unreachable or returned an error."""

    def __init__(self, detail: str = "SpaceX API request failed") -> None:
        self.detail = detail


class ResourceNotFoundError(Exception):
    """Requested resource (launch, rocket, launchpad) does not exist."""

    def __init__(self, resource: str, resource_id: str) -> None:
        self.detail = f"{resource} '{resource_id}' not found"


class CacheError(Exception):
    """Cache read/write failed (corruption, permissions, etc.)."""

    def __init__(self, detail: str = "Cache operation failed") -> None:
        self.detail = detail
