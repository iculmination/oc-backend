from app.engine.effects.base import EffectBase


class HiddenEffect(EffectBase):
    def modify_incoming_damage(self, damage):
        return 0

    def modify_outgoing_damage(self, damage):
        return damage * 0.5
