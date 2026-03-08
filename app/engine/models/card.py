from dataclasses import dataclass, field
from uuid import UUID
from typing import list


@dataclass
class CardState:
    id: UUID
    card_id: UUID
    owner_id: UUID

    attack: int
    health: int
    energy: int

    statuses: list[str] = field(default_factory=list)
