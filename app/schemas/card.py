from pydantic import BaseModel
from uuid import UUID
from app.enums.card import CardAbilities, CardNature

class CardSchema(BaseModel):
    id: UUID
    name: str
    attack: int
    health: int
    max_health: int
    ability: CardAbilities
    nature: CardNature 