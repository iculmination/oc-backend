from dataclasses import dataclass, field
from uuid import UUID
from typing import list

from .card_instance import CardInstance


@dataclass
class PlayerState:
    id: UUID
    hp: int

    deck: list[CardInstance] = field(default_factory=list)
    hand: list[CardInstance] = field(default_factory=list)
    board: list[CardInstance] = field(default_factory=list)