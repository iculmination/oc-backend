from app.engine.events.base import EventBase
from app.enums.card import CardNature, CardEffects


class BloodRainEvent(EventBase):
    affects_nature = CardNature.HUMAN
    applies_effect = CardEffects.INSANITY