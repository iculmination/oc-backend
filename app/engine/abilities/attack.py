from app.engine.abilities.base import AbilityBase
from app.engine.utils.targeting import get_enemy_by_id, get_random_enemy
from app.engine.effects.registry import EFFECT_REGISTRY


class AttackAbility(AbilityBase):
    def execute(self, state, card, target_id=None):
        target = (
            get_enemy_by_id(state, card.owner_id, target_id)
            if target_id is not None
            else get_random_enemy(state, card.owner_id)
        )
        if target:
            damage = card.attack

            for effect in target.statuses:
                damage = EFFECT_REGISTRY[effect].modify_incoming_damage(damage)

            for effect in card.statuses:
                damage = EFFECT_REGISTRY[effect].modify_outgoing_damage(damage)

            target.health -= damage
            card.last_action = f"Attacked {target.name} for {damage} damage."
            return card.last_action
        else:
            card.last_action = "Tried to attack, but no enemy target was available."
            return card.last_action
