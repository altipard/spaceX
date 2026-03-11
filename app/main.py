from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.exceptions import CacheError, ResourceNotFoundError, SpaceXAPIError
from app.routers import launches
from app.services.cache import CacheService
from app.services.spacex_client import SpaceXClient


# lifespan replaces the old @app.on_event("startup") / ("shutdown") pattern.
# everything BEFORE yield runs once at startup, everything AFTER at shutdown.
# services created here are singletons — one instance for the whole app lifetime.
# we store them on app.state so that dependency functions can grab them per-request
# via request.app.state (see dependencies.py).
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    # startup — create shared services once, store on app.state.
    # this is the FastAPI-idiomatic way to do singletons:
    # instead of __new__ tricks on the class, let the framework manage the lifecycle.
    app.state.cache = CacheService(settings)
    app.state.spacex_client = SpaceXClient(settings)

    yield  # app is running and serving requests between startup and shutdown

    # shutdown — clean up resources (close DB connections, HTTP clients, etc.)
    app.state.cache.close()


app = FastAPI(
    title="SpaceX Launch Tracker",
    description="API backend consuming SpaceX v4 API with caching and analytics",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(launches.router)

# services raise the exceptions, handlers map them to HTTP responses.
# routers never catch exceptions manually — they bring them up to here.


@app.exception_handler(ResourceNotFoundError)
async def resource_not_found_handler(request: Request, exc: ResourceNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": exc.detail, "status_code": 404})


@app.exception_handler(SpaceXAPIError)
async def spacex_api_error_handler(request: Request, exc: SpaceXAPIError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": exc.detail, "status_code": 502})


@app.exception_handler(CacheError)
async def cache_error_handler(request: Request, exc: CacheError) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": exc.detail, "status_code": 500})


@app.get("/")
async def root():
    return {"message": "SpaceX Launch Tracker API"}
