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
    duration: int