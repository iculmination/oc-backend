from app.enums.card import CardEffects, CardNature


class EventBase:
    affects_nature: CardNature
    applies_effect: CardEffects

    def apply(self, state):
        for player in state.players.values():
            for card in player.board:
                if card.nature == self.affects_nature:
                    if self.applies_effect not in card.effects:
                        card.effects.append(self.applies_effect)

    def remove(self, state):
        for player in state.players.values():
            for card in player.board:
                if card.nature == self.affects_nature:
                    if self.applies_effect in card.effects:
                        card.effects.remove(self.applies_effect)

    def on_card_act(self, state, card):
        pass
