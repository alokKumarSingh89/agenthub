import asyncio
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.api.app.application import create_application
from apps.api.app.config import Settings
from apps.api.app.health import get_database
from packages.database import Database


class HealthyDatabase:
    async def check_connection(self) -> None:
        return None


class UnavailableDatabase:
    async def check_connection(self) -> None:
        raise ConnectionError("Database is unavailable")


def create_test_application(
    database: object,
) -> tuple[TestClient, FastAPI, Database]:
    settings = Settings(
        database_url="postgresql+asyncpg://agenthub:agenthub@localhost:5432/agenthub",
    )

    real_database = Database(
        database_url=settings.database_url,
    )

    application = create_application(
        settings=settings,
        database=real_database,
    )

    async def override_database() -> AsyncGenerator[object, None]:
        yield database

    application.dependency_overrides[get_database] = override_database

    return TestClient(application), application, real_database


def test_health() -> None:
    client, _, database = create_test_application(
        HealthyDatabase(),
    )

    try:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {
            "status": "ok",
        }
    finally:
        asyncio.run(database.dispose())


def test_readiness_when_database_is_available() -> None:
    client, _, database = create_test_application(
        HealthyDatabase(),
    )

    try:
        response = client.get("/health/ready")

        assert response.status_code == 200
        assert response.json() == {
            "status": "ready",
            "checks": {
                "database": "ok",
            },
        }
    finally:
        asyncio.run(database.dispose())


def test_readiness_when_database_is_unavailable() -> None:
    client, _, database = create_test_application(
        UnavailableDatabase(),
    )

    try:
        response = client.get("/health/ready")

        assert response.status_code == 503
        assert response.json() == {
            "status": "not_ready",
            "checks": {
                "database": "failed",
            },
        }
    finally:
        asyncio.run(database.dispose())
