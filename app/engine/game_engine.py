import random
from loguru import logger

from app.enums.game import GameStatus
from app.enums.card import CardEffects

from app.engine.events.registry import EVENTS_REGISTRY
from app.engine.abilities.registry import ABILITY_REGISTRY


class GameEngine:

    def process_turn(self, state, with_events=True):
        if state.status == GameStatus.FINISHED:
            logger.info("Game already finished. Skipping turn.")
            return state

        logger.info(f"--- Actor turn: {state.active_player} ---")
        if with_events:
            self.events_phase(state)
        self.cards_phase(state)
        self.cleanup_phase(state)
        self.end_phase(state)
        self.advance_active_player(state)
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
        for player_id, player in state.players.items():
            for card in player.board:
                if card.health > 0:
                    players_alive.append(player_id)
                    break

        if len(players_alive) == 1:
            state.status = GameStatus.FINISHED
            state.winner_id = players_alive[0]
            return

        if len(players_alive) == 0:
            state.status = GameStatus.FINISHED
            state.winner_id = None

    def cards_act(self, state):
        player = state.players[state.active_player]
        self.expire_start_of_turn_effects(player)
        for card in player.board:
            if card.is_alive():
                ABILITY_REGISTRY[card.ability].execute(state, card)

    def play_selected_action(self, state, card_id, target_id=None):
        if state.status == GameStatus.FINISHED:
            return "Game is already finished."

        player = state.players[state.active_player]
        self.expire_start_of_turn_effects(player)

        acting_card = None
        for card in player.board:
            if str(card.id) == str(card_id):
                acting_card = card
                break

        if acting_card is None:
            return "Selected card is not on the active player's board."

        if not acting_card.is_alive():
            return f"{acting_card.name} cannot act because it is not alive."

        action_text = ABILITY_REGISTRY[acting_card.ability].execute(
            state, acting_card, target_id=target_id
        )

        self.cleanup_phase(state)
        self.end_phase(state)
        self.advance_active_player(state)

        return action_text

    def expire_start_of_turn_effects(self, player):
        for card in player.board:
            if CardEffects.HIDDEN in card.statuses:
                card.statuses = [status for status in card.statuses if status != CardEffects.HIDDEN]

    def cleanup_dead_cards(self, state):
        for player in state.players.values():
            dead = [c for c in player.board if not c.is_alive()]
            player.board = [c for c in player.board if c.is_alive()]

    def process_events(self, state):
        for event in list(state.active_events):
            if event.duration <= 0:
                event.remove(state)
                state.active_events.remove(event)
                continue
            event.duration -= 1

    def add_random_event(self, state):
        if random.random() < 0.25:
            event_cls = random.choice(list(EVENTS_REGISTRY.values()))
            event = event_cls()
            event.apply(state)
            state.active_events.append(event)

    def advance_active_player(self, state):
        if state.status == GameStatus.FINISHED:
            return

        player_ids = list(state.players.keys())
        if not player_ids:
            return

        current_index = player_ids.index(state.active_player)
        next_index = (current_index + 1) % len(player_ids)
        state.active_player = player_ids[next_index]


    def shuffle_start_cards(self, state):
        raise NotImplementedError("Start-card pool is not wired yet.")
