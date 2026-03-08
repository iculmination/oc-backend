from dataclasses import dataclass, field
from uuid import UUID
from typing import dict

from .player import PlayerState
from .event import EventState
from .card import CardState


@dataclass
class GameState:
    id: UUID
    turn: int
    active_player: UUID

    players: dict[UUID, PlayerState] = field(default_factory=dict)
    active_events: list[EventState] = field(default_factory=list)
