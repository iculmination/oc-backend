class EffectResolver:

    def resolve(self, state, effect):

        if effect["type"] == "damage":
            self.damage(state, effect)

        if effect["type"] == "apply_status":
            self.apply_status(state, effect)

    def damage(self, state, effect):

        target = self.find_card(state, effect["target"])

        target.health -= effect["value"]

    def apply_status(self, state, effect):

        for player in state.players.values():

            for card in player.board:

                card.statuses.append(effect["status"])
