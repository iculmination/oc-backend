import math

from app.engine.abilities.base import AbilityBase
from app.engine.utils.targeting import get_ally_by_id, get_random_ally


class BuffAbility(AbilityBase):
    def execute(self, state, card, target_id=None):
        target = (
            get_ally_by_id(state, card.owner_id, target_id)
            if target_id is not None
            else get_random_ally(state, card.owner_id)
        )
        if target:
            old_attack = target.attack
            target.attack = math.ceil(target.attack * 1.5)
            card.last_action = (
                f"Buffed {target.name}: attack {old_attack} -> {target.attack}."
            )
            return card.last_action
        else:
            card.last_action = "Tried to buff, but no ally target was available."
            return card.last_action
