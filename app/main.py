from fastapi import FastAPI

app = FastAPI(
    title="SpaceX Launch Tracker",
    description="API backend consuming SpaceX v4 API with caching and analytics",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {"message": "SpaceX Launch Tracker API"}
