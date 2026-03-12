from app.engine.abilities.base import AbilityBase
from app.engine.utils.targeting import get_random_enemy
from app.engine.effects.registry import EFFECT_REGISTRY


class AttackAbility(AbilityBase):
    def execute(self, state, card):
        target = get_random_enemy(state, card.owner_id)
        if target:
            damage = card.attack

            for effect in target.effects:
                damage = EFFECT_REGISTRY[effect].modify_incoming_damage(damage)

            for effect in card.effects:
                damage = EFFECT_REGISTRY[effect].modify_outgoing_damage(damage)

            target.health -= damage
