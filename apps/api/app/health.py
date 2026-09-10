from collections.abc import AsyncGenerator
from typing import Protocol

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse


class DatabaseHealthChecker(Protocol):
    async def check_connection(self) -> None:
        ...


async def get_database(
    request: Request,
) -> AsyncGenerator[DatabaseHealthChecker, None]:
    database = request.app.state.database
    yield database


router = APIRouter()


@router.get("")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
    }


@router.get("/ready")
async def readiness(
    database: DatabaseHealthChecker = Depends(get_database),
) -> JSONResponse:
    try:
        await database.check_connection()
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "checks": {
                    "database": "failed",
                },
            },
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "ready",
            "checks": {
                "database": "ok",
            },
        },
    )