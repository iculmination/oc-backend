from app.engine.events.base import EventBase
from app.enums.card import CardNature, CardEffects


class SolarFlareEvent(EventBase):
    affects_nature = CardNature.CREATURE
    applies_effect = CardEffects.INSANITY
