# dependency factories for FastAPI's Depends() injection.
# never done this in python before :-)
# routers import these — never instantiate services directly.


from app.config import get_settings, Settings


def get_settings_dep() -> Settings:
    return get_settings()