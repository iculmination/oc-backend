from dataclasses import dataclass
from uuid import UUID

from app.enums.card import CardEffects

@dataclass
class EventState:
    id: UUID
    name: str
    description: str
    rarity: str
    status: str
    source: str
    effect: str
    applies_effect: CardEffects
    affects_nature: str
    duration: int
