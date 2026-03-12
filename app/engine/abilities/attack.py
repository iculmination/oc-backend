from app.engine.abilities.base import AbilityBase
from app.enums.card import CardEffects


class AttackAbility(AbilityBase):
    def execute(self, state, card):
        target = engine.get_random_enemy(state, card.owner_id)
        if target:
            damage = card.attack
            if CardEffects.INSANITY in target.effects:
                damage *= 1.5
            target.health -= damage
