from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api.dependencies import current_user
from app.schemas.game import (
    GameListResponse,
    GameStartResponse,
    GameStateResponse,
    GameSummary,
    GameTurnRequest,
)
from app.services.game_runtime import game_runtime_service

router = APIRouter(prefix="/game", tags=["Game"])


@router.post("/start-vs-bot", response_model=GameStartResponse)
async def start_vs_bot(user: current_user):
    return await game_runtime_service.start_vs_bot(user.user_id)


@router.get("/active", response_model=GameSummary)
async def get_active_game(user: current_user):
    active = await game_runtime_service.get_active_game(user.user_id)
    if active is None:
        raise HTTPException(status_code=404, detail="No active game found")
    return active


@router.get("/my", response_model=GameListResponse)
async def list_my_games(user: current_user):
    return await game_runtime_service.list_games(user.user_id)


@router.post("/{game_id}/turn", response_model=GameStateResponse)
async def play_turn(game_id: UUID, payload: GameTurnRequest, user: current_user):
    return await game_runtime_service.play_turn(
        game_id=game_id,
        user_id=user.user_id,
        card_id=payload.card_id,
        target_id=payload.target_id,
    )


@router.get("/{game_id}", response_model=GameStateResponse)
async def get_game_state(game_id: UUID, user: current_user):
    return await game_runtime_service.get_state(game_id, user.user_id)


@router.post("/{game_id}/surrender", response_model=GameStateResponse)
async def surrender_game(game_id: UUID, user: current_user):
    return await game_runtime_service.surrender(game_id, user.user_id)


@router.post("/{game_id}/end", response_model=GameStateResponse)
async def end_game(game_id: UUID, user: current_user):
    return await game_runtime_service.end_game(game_id, user.user_id)
