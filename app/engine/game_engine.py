import random
from loguru import logger

from app.enums.game import GameStatus
from app.engine.mock.event import blood_rain, plague, solar_flare


class GameEngine:

    def process_turn(self, state):
        logger.info(f"--- Turn {state.turn} ---")
        state.turn += 1
        self.check_if_game_ended(state)
        self.add_random_event(state)
        self.process_events(state)
        self.cards_act(state)
        self.cleanup_dead_cards(state)
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

    def find_card(self, state, card_id):
        for player in state.players.values():
            for card in player.board:
                if str(card.id) == card_id:
                    return card
        raise ValueError("Card not found")

    def remove_card(self, state, card):
        owner = state.players[card.owner_id]
        owner.board = [c for c in owner.board if c.id != card.id]

    def end_turn(self, state):
        state.turn += 1
        players = list(state.players.keys())
        current_index = players.index(state.active_player)
        next_index = (current_index + 1) % len(players)
        state.active_player = players[next_index]
        return state

    def cards_act(self, state):
        for player in state.players.values():
            for card in player.board:
                if not card.is_alive():
                    continue
                self.resolve_card_action(state, card)

    def resolve_card_action(self, state, card):
        if card.ability == "attack":
            target = self.get_random_enemy(state, card.owner_id)
            if target:
                target.health -= card.attack
                logger.debug(
                    f"{(card.name)} attack → {(target.name)} (-{card.attack}) → {target.health} HP"
                )
            else:
                logger.debug(f"{(card.name)} attack → no target")

        if card.ability == "heal":
            target = self.get_random_ally(state, card.owner_id)
            if target:
                old_hp = target.health
                target.health = min(target.max_health, target.health + card.attack)
                logger.debug(
                    f"{(card.name)} heal → {(target.name)} (+{card.attack}) {old_hp}→{target.health} HP"
                )
            else:
                logger.debug(f"{(card.name)} heal → no target")

    def get_random_enemy(self, state, player_id):
        enemies = []
        for pid, player in state.players.items():
            if pid == player_id:
                continue
            enemies.extend(player.board)
        return random.choice(enemies) if enemies else None

    def get_random_ally(self, state, player_id):
        player = state.players[player_id]
        return random.choice(player.board) if player.board else None

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
                logger.debug(f"Event {event.name} expired")
                continue
            event.duration -= 1
            for player in state.players.values():
                for card in player.board:
                    if card.nature == event.affects_nature:
                        if event.applies_effect not in card.statuses:
                            card.statuses.append(event.applies_effect)
                            logger.debug(
                                f"{event.name} → {card.nature} {card.name} gained {event.applies_effect}"
                            )
                        else:
                            logger.debug(
                                f"{event.name} → {card.nature} {card.name} already has {event.applies_effect}"
                            )


    def play_card(self, state, player_id, card_id):
        player = state.players[player_id]
        card = next(c for c in player.deck if c.id == card_id)
        player.board.append(card)

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
