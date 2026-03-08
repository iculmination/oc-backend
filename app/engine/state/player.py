from dataclasses import dataclass, field
from uuid import UUID

from .card import CardState


@dataclass
class PlayerState:
    id: UUID

    deck: list[CardState] = field(default_factory=list)
    board: list[CardState] = field(default_factory=list)
