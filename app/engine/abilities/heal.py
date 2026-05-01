from app.engine.abilities.base import AbilityBase
from app.engine.utils.targeting import get_ally_by_id, get_random_ally


class HealAbility(AbilityBase):
    def execute(self, state, card, target_id=None):
        target = (
            get_ally_by_id(state, card.owner_id, target_id)
            if target_id is not None
            else get_random_ally(state, card.owner_id)
        )
        if target:
            old_health = target.health
            target.health = min(target.max_health, target.health + card.attack)
            restored = target.health - old_health
            card.last_action = f"Healed {target.name} for {restored} HP."
            return card.last_action
        else:
            card.last_action = "Tried to heal, but no ally target was available."
            return card.last_action
