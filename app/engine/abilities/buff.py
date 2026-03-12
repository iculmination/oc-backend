from app.engine.abilities.base import AbilityBase
from app.engine.utils.targeting import get_random_ally


class BuffAbility(AbilityBase):
    def execute(self, state, card):
        target = get_random_ally(state, card.owner_id)
        if target:
            target.attack *= 1.5
