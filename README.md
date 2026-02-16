# SpaceX Launch Tracker API

FastAPI backend that consumes the [SpaceX v4 API](https://api.spacexdata.com/v4).

## Quick Start (Docker)

```bash
cp .env.example .env
docker-compose up --build
```

## Local Development

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
cp .env.example .env
# Set CACHE_DIR=data in .env (instead of /app/data)
uv sync                          # install all deps including dev
uv run uvicorn app.main:app --reload
```

### Common Commands

```bash
uv run pytest                    # run tests
uv run ruff check .              # lint
uv run ruff format .             # format
uv add <package>                 # add a dependency
uv add --group dev <package>     # add a dev dependency
uv lock --upgrade                # upgrade all deps
```

API: `http://localhost:8000`
Swagger: `http://localhost:8000/docs`

## Configuration

See `.env.example` for all environment variables.
