import random
from loguru import logger

from app.enums.game import GameStatus

from app.engine.events.registry import EVENTS_REGISTRY
from app.engine.abilities.registry import ABILITY_REGISTRY


class GameEngine:

    def process_turn(self, state):
        logger.info(f"--- Turn {state.turn} ---")
        state.turn += 1
        self.events_phase(state)
        self.cards_phase(state)
        self.cleanup_phase(state)
        self.end_phase(state)
        return state

    def events_phase(self, state):
        self.add_random_event(state)
        self.process_events(state)

    def cards_phase(self, state):
        self.cards_act(state)

    def cleanup_phase(self, state):
        self.cleanup_dead_cards(state)

    def end_phase(self, state):
        self.check_if_game_ended(state)

    def check_if_game_ended(self, state):
        players_alive = []
        for player in state.players.values():
            for card in player.board:
                if card.health > 0:
                    players_alive.append(player)
                    break

        if len(players_alive) == 1 or len(players_alive) == 0:
            state.status = GameStatus.FINISHED

    def cards_act(self, state):
        for player in state.players.values():
            for card in player.board:
                if card.is_alive():
                    ABILITY_REGISTRY[card.ability].execute(state, card)

    def cleanup_dead_cards(self, state):
        for player in state.players.values():
            dead = [c for c in player.board if not c.is_alive()]
            player.board = [c for c in player.board if c.is_alive()]

    def process_events(self, state):
        for event in state.active_events:
            if event.duration <= 0:
                event.remove(state)
                continue
            event.duration -= 1

    def add_random_event(self, state):
        if random.random() < 0.25:
            event = random.choice(list(EVENTS_REGISTRY.values()))
            if type(event) not in [type(e) for e in state.active_events]:
                event.apply(state)
                

    def shuffle_start_cards(self, state):
        cards = random.sample(ALL_CARDS, 5)

        state.available_choices = cards
