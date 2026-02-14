# SpaceX Launch Tracker API

FastAPI backend that consumes the [SpaceX v4 API](https://api.spacexdata.com/v4).

## Quick Start (Docker)

```bash
cp .env.example .env
docker-compose up --build
```

## Local Development

```bash
cp .env.example .env
# Set CACHE_DIR=data in .env (instead of /app/data)
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

API: `http://localhost:8000`
Swagger: `http://localhost:8000/docs`

## Configuration

See `.env.example` for all environment variables.
