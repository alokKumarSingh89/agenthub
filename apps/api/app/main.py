from fastapi import FastAPI

from apps.api.app.application import create_application
from apps.api.app.config import get_settings
from packages.database import Database

settings = get_settings()
database = Database(database_url=settings.database_url)

app: FastAPI = create_application(
    settings=settings,
    database=database,
)
