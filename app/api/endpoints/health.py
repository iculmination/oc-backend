from fastapi import APIRouter
from app.schemas.health import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=HealthResponse)
async def health():
    return HealthResponse(status=200, message="The server is running")
