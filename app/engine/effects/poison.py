from app.engine.effects.base import EffectBase


class PoisonEffect(EffectBase):
    def modify_incoming_damage(self, damage):
        return damage

    def modify_outgoing_damage(self, damage):
        return damage - 1
