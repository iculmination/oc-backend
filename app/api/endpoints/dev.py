from fastapi import APIRouter
from app.engine.test.game import test_game_engine

router = APIRouter(prefix="/dev", tags=["Dev"])


@router.get("/game")
async def test_game():
    return test_game_engine()
