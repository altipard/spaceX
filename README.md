# SpaceX Launch Tracker API

FastAPI backend that consumes the [SpaceX v4 API](https://github.com/r-spacex/SpaceX-API) with local caching and some analytics on top.

## Setup

You'll need [uv](https://docs.astral.sh/uv/) and [Task](https://taskfile.dev/installation/).

```bash
cp .env.example .env
task install
task run
```

That's it. API runs on `http://localhost:8000`, Swagger docs at `/docs`.

Run `task` to see all available commands — `task test`, `task lint`, `task fix`, etc.

## What it does

The app fetches data from the SpaceX v4 API and caches it locally in SQLite so we're not hammering their servers on every request. Cache TTL is configurable via `.env` (defaults to 5 minutes).

### Endpoints

**Launches** — `GET /launches` and `GET /launches/{id}`

The list endpoint supports a bunch of query filters: `start_date`, `end_date`, `rocket_id`, `launchpad_id`, `success`. You can also pass `export=csv` to get a CSV download instead of JSON. All filtering happens in-memory on the cached dataset, which is fine for ~200 launches.

**Rockets** — `GET /rockets` and `GET /rockets/{id}`

**Launchpads** — `GET /launchpads` and `GET /launchpads/{id}`

**Statistics** — three endpoints under `/statistics/`:
- `/success-rate` — success/failure rate grouped by rocket
- `/launches-per-site` — how many launches per launchpad
- `/launch-frequency` — launches per month and per year

**Cache** — `DELETE /cache` clears everything. You can also pass `?refresh=true` on any list endpoint to bypass the cache for that request.

## Project structure

```
app/
├── main.py              # app + exception handlers
├── config.py            # settings via pydantic-settings
├── models.py            # Launch, Rocket, Launchpad
├── exceptions.py
├── dependencies.py
├── routers/             # one file per resource + statistics + cache
└── services/
    ├── spacex_client.py # httpx wrapper for the SpaceX API
    ├── cache.py         # SQLite cache with TTL
    └── statistics.py    # pure functions for the stats calculations
```

## Configuration

See `.env.example` — you can override `SPACEX_BASE_URL`, `CACHE_TTL`, `CACHE_DIR`, `HOST`, and `PORT`.
