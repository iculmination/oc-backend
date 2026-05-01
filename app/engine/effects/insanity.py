from app.engine.effects.base import EffectBase


class InsanityEffect(EffectBase):
    def modify_incoming_damage(self, damage):
        return damage * 2
        
    def modify_outgoing_damage(self, damage):
        return damage * 1.5
