import random
from loguru import logger

from app.enums.game import GameStatus

from app.engine.mock.event import blood_rain, plague, solar_flare
from app.engine.abilities.registry import ABILITY_REGISTRY


class GameEngine:

    def process_turn(self, state):
        logger.info(f"--- Turn {state.turn} ---")
        state.turn += 1
        self.add_random_event(state)
        self.process_events(state)
        self.cards_act(state)
        self.cleanup_dead_cards(state)
        self.check_if_game_ended(state)
        return state

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
            if dead:
                logger.debug(f"cleanup: removed {[(c.name) for c in dead]}")
            player.board = [c for c in player.board if c.is_alive()]

    def process_events(self, state):
        logger.debug(f"Processing {len(state.active_events)} events")
        for event in state.active_events:
            if event.duration <= 0:
                state.active_events.remove(event)
                logger.debug(f"Event {event.name} has ended")
                self.remove_effect_from_event(state, event)
                continue
            logger.debug(f"{event.duration} more rounds with {event.name} left")
            event.duration -= 1
            self.apply_effect_from_event(state, event)

    def apply_effect_from_event(self, state, event):
        for player in state.players.values():
            for card in player.board:
                if card.nature == event.affects_nature:
                    if event.applies_effect not in card.effects:
                        card.effects.append(event.applies_effect)
                        logger.debug(
                            f"{event.name} started → {card.nature} {card.name} gained {event.applies_effect}"
                        )
                    else:
                        logger.debug(
                            f"{event.name} started → {card.nature} {card.name} already has {event.applies_effect}"
                        )

    def remove_effect_from_event(self, state, event):
        for player in state.players.values():
            for card in player.board:
                if card.nature == event.affects_nature:
                    if event.applies_effect in card.effects:
                        card.effects.remove(event.applies_effect)
                        logger.debug(
                            f"{event.name} ended → {card.nature} {card.name} lost {event.applies_effect} effect"
                        )
                    else:
                        logger.debug(
                            f"{event.name} ended → {card.nature} {card.name} didn't have {event.applies_effect}"
                        )

    def add_random_event(self, state):
        if random.random() < 0.25:

            event = random.choice([blood_rain(), plague(), solar_flare()])
            if event in state.active_events:
                logger.info(
                    f"Random event ({event.name}) already existed. No events will be applied this round."
                )
            else:
                logger.info(
                    f"Adding random event: {event.name} (duration: {event.duration}, effect: {event.description})"
                )
                state.active_events.append(event)
