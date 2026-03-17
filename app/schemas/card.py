from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from app.enums.card import CardAbilities, CardNature


class CardSchema(BaseModel):
    name: str
    attack: int
    max_health: int
    ability: CardAbilities
    nature: CardNature

class CardReadSchema(CardSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime