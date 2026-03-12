from app.engine.abilities.base import AbilityBase
from app.enums.card import CardEffects


class HideAbility(AbilityBase):
    def execute(self, state, card):
        card.effects.append(CardEffects.HIDDEN)
