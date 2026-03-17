from fastapi import APIRouter
from app.schemas.health import HealthResponse
from app.db.session import async_session
from sqlalchemy import text

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=HealthResponse)
async def health():
    return HealthResponse(status=200, message="The server is running")


@router.get("/db")
async def db_health():
    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
            return HealthResponse(status=200, message="The database is running")
    except Exception as e:
        return HealthResponse(status=500, message=f"The database is not running: {e}")
