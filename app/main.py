from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.exceptions import ResourceNotFoundError, SpaceXAPIError, CacheError

app = FastAPI(
    title="SpaceX Launch Tracker",
    description="API backend consuming SpaceX v4 API with caching and analytics",
    version="0.1.0",
)


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
