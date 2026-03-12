from app.engine.events.base import EventBase
from app.enums.card import CardNature, CardEffects


class PlagueEvent(EventBase):
    affects_nature = CardNature.ROBOT
    applies_effect = CardEffects.INSANITY
