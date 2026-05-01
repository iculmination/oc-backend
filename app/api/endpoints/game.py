from uuid import UUID

from fastapi import APIRouter

from app.schemas.game import GameStartResponse, GameStateResponse, GameTurnRequest
from app.services.game_runtime import game_runtime_service

router = APIRouter(prefix="/game", tags=["Game"])


@router.post("/start-vs-bot", response_model=GameStartResponse)
async def start_vs_bot():
    return game_runtime_service.start_vs_bot()


@router.post("/{game_id}/turn", response_model=GameStateResponse)
async def play_turn(game_id: UUID, payload: GameTurnRequest):
    return game_runtime_service.play_turn(
        game_id=game_id,
        player_id=payload.player_id,
        card_id=payload.card_id,
        target_id=payload.target_id,
    )


@router.get("/{game_id}", response_model=GameStateResponse)
async def get_game_state(game_id: UUID):
    return game_runtime_service.get_state(game_id)
