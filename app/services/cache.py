import json
import sqlite3
import threading
import time

from app.config import Settings
from app.exceptions import CacheError


class CacheService:
    """SQLite-backed key-value cache with TTL support.

    Each endpoint path (e.g. /launches, /rockets/abc123) gets its own
    cache entry.  Stale entries are served only when the TTL hasn't
    expired yet — after that we return None and let the caller re-fetch.

    Singleton pattern — only one instance exists per process.
    repeated calls return the same instance.
    """

    _instance: "CacheService | None" = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, settings: Settings) -> "CacheService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, settings: Settings) -> None:
        if hasattr(self, "_initialised"):
            return
        self._initialised = True

        self._ttl = settings.cache_ttl
        db_path = settings.cache_dir / "spacex_cache.db"

        try:
            self._conn = sqlite3.connect(str(db_path), check_same_thread=False)
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cache (
                    key   TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    ts    REAL NOT NULL
                )
                """
            )
            self._conn.commit()
        except sqlite3.Error as exc:
            raise CacheError(f"Failed to initialize cache database: {exc}") from exc

    def get(self, key: str) -> list[dict] | dict | None:
        """Return cached JSON for *key*, or None if missing / expired."""
        try:
            row = self._conn.execute(
                "SELECT value, ts FROM cache WHERE key = ?", (key,)
            ).fetchone()
        except sqlite3.Error as exc:
            raise CacheError(f"Cache read failed: {exc}") from exc

        if row is None:
            return None

        value, ts = row
        if time.time() - ts > self._ttl:
            return None

        return json.loads(value)

    def set(self, key: str, data: list[dict] | dict) -> None:
        """Write JSON data into cache, overwriting any previous entry."""
        try:
            with self._conn:
                self._conn.execute(
                    """
                    INSERT INTO cache (key, value, ts)
                    VALUES (?, ?, ?)
                    ON CONFLICT(key) DO UPDATE SET value = excluded.value, ts = excluded.ts
                    """,
                    (key, json.dumps(data), time.time()),
                )
        except sqlite3.Error as exc:
            raise CacheError(f"Cache write failed: {exc}") from exc

    def clear(self) -> None:
        """Drop all cache entries."""
        try:
            with self._conn:
                self._conn.execute("DELETE FROM cache")
        except sqlite3.Error as exc:
            raise CacheError(f"Cache clear failed: {exc}") from exc