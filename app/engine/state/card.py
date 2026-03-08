from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class CardState:

    id: UUID
    card_id: UUID
    owner_id: UUID

    name: str

    attack: int
    health: int
    max_health: int

    ability: str

    nature: str
    cooldown: int = 0

    statuses: list[str] = field(default_factory=list)

    def is_alive(self):
        return self.health > 0
