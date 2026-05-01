from uuid import UUID

from pydantic import BaseModel


class GameEventState(BaseModel):
    name: str
    duration: int


class GameCardState(BaseModel):
    id: UUID
    name: str
    health: int
    max_health: int
    attack: int
    ability: str
    statuses: list[str]
    last_action: str | None


class GamePlayerState(BaseModel):
    cards_alive: int
    cards: list[GameCardState]


class GameLogEntry(BaseModel):
    round: int
    actor: str
    text: str


class GameSnapshot(BaseModel):
    status: str
    turn: int
    active_player: UUID
    winner_id: UUID | None
    active_events: list[GameEventState]
    players: dict[UUID, GamePlayerState]
    battle_log: list[GameLogEntry]


class GameStartResponse(BaseModel):
    game_id: UUID
    player_id: UUID
    bot_id: UUID
    state: GameSnapshot


class GameTurnRequest(BaseModel):
    card_id: UUID
    target_id: UUID | None = None


class GameStateResponse(BaseModel):
    game_id: UUID
    player_id: UUID
    bot_id: UUID
    state: GameSnapshot


class GameSummary(BaseModel):
    game_id: UUID
    status: str
    turn: int
    winner_player_id: UUID | None
    updated_at: str


class GameListResponse(BaseModel):
    games: list[GameSummary]
