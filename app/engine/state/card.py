from dataclasses import dataclass, field
from uuid import UUID

from app.enums.card import CardFaction, CardNature, CardSpecialty, CardEffects


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

    nature: CardNature
    cooldown: int = 0
    effects: list[CardEffects] = field(default_factory=list)

    def is_alive(self):
        return self.health > 0
