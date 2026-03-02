from datetime import datetime

from pydantic import BaseModel, Field


# ... SpaceX Api response model ...


class Launch(BaseModel):
    # model_config = {"extra": "ignore"}
    # is obsolete as this is default behavioe in pydantic v2,
    # so: extra passed values are ignored
    id: str
    name: str
    flight_number: int
    date_utc: datetime
    date_local: str
    date_precision: str
    rocket: str  # uuid, resolved to name later
    launchpad: str  # uuid, resolved to name later
    success: bool | None = None
    details: str | None = None
    upcoming: bool


class Rocket(BaseModel):
    id: str
    name: str
    type: str
    active: bool
    country: str
    company: str
    description: str
    wikipedia: str
    cost_per_launch: int
    success_rate_pct: int
    first_flight: str
    flickr_images: list[str] = Field(default_factory=list)


class Launchpad(BaseModel):
    id: str
    name: str
    full_name: str
    status: str
    locality: str
    region: str
    latitude: float
    longitude: float
    launch_attempts: int
    launch_successes: int
    rockets: list[str] = Field(default_factory=list)
    launches: list[str] = Field(default_factory=list)