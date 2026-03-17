from app.enums.card import CardEffects, CardNature
from loguru import logger


class EventBase:
    affects_nature: CardNature
    applies_effect: CardEffects

    def apply(self, state):
        for player in state.players.values():
            for card in player.board:
                if card.nature == self.affects_nature:
                    if self.applies_effect not in card.statuses:
                        card.statuses.append(self.applies_effect)

    def remove(self, state):
        for player in state.players.values():
            for card in player.board:
                if card.nature == self.affects_nature:
                    if self.applies_effect in card.statuses:
                        card.statuses.remove(self.applies_effect)

    def on_card_act(self, state, card):
        pass
