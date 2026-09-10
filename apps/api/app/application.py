from fastapi import FastAPI

from apps.api.app.config import Settings
from apps.api.app.health import router as health_router
from packages.database import Database


def create_application(settings: Settings, database: Database) -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Enterprise AI Agent Platform",
    )
    app.state.settings = settings
    app.state.database = database

    app.include_router(health_router, prefix="/health", tags=["Health"])
    return app
