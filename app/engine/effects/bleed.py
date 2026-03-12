from app.engine.effects.base import EffectBase


class BleedEffect(EffectBase):
    def modify_incoming_damage(self, damage):
        return damage + 1

    def modify_outgoing_damage(self, damage):
        return damage
