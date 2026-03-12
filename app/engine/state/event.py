from dataclasses import dataclass
from uuid import UUID


@dataclass
class EventState:
    id: UUID
    name: str
    description: str
    rarity: str
    status: str
    source: str
    effect: str
    applies_effect: str
    affects_nature: str
    duration: int
