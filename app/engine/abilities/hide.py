from app.engine.abilities.base import AbilityBase
from app.enums.card import CardEffects


class HideAbility(AbilityBase):
    def execute(self, state, card, target_id=None):
        if CardEffects.HIDDEN not in card.statuses:
            card.statuses.append(CardEffects.HIDDEN)
            card.last_action = "Activated stealth for one cycle."
        else:
            card.last_action = "Stealth was already active."
        return card.last_action
