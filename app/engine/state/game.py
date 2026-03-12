from dataclasses import dataclass, field
from uuid import UUID

from app.enums.game import GameStatus
from .player import PlayerState


@dataclass
class GameState:
    id: UUID

    turn: int
    active_player: UUID

    players: dict[UUID, PlayerState]

    active_events: list[dict] = field(default_factory=list)
    status: GameStatus = GameStatus.ONGOING