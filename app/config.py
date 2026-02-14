from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


# Pydantic Settings priority (highest wins):
#   1. System environment variable   (export CACHE_TTL=600)
#   2. .env file                     (CACHE_TTL=600)
#   3. Default value below           (300)
# Fields without a default are required — app won't start if missing.


class Settings(BaseSettings):
    spacex_base_url: str = "https://api.spacexdata.com/v4"
    cache_ttl: int = 300  # seconds
    cache_dir: Path = Path("data")  # overridden in Docker via env var
    host: str = "0.0.0.0"
    port: int = 8000

    # Without env_file, only system env vars would be read — .env file ignored.
    # env_file_encoding ensures correct handling of special characters.
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache  # singleton — same Settings instance reused across the app
def get_settings() -> Settings:
    return Settings()