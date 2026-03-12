class EffectBase:
    def modify_incoming_damage(self, damage):
        raise NotImplementedError

    def modify_outgoing_damage(self, damage):
        raise NotImplementedError
