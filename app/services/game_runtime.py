from uuid import UUID, uuid4

from fastapi import HTTPException

from app.engine.game_engine import GameEngine
from app.engine.mock.cards import draft_random_cards
from app.engine.state.game import GameState
from app.engine.state.player import PlayerState
from app.enums.game import GameStatus
from app.schemas.game import (
    GameCardState,
    GameEventState,
    GameLogEntry,
    GamePlayerState,
    GameSnapshot,
    GameStartResponse,
    GameStateResponse,
)


class GameRuntimeService:
    def __init__(self):
        self._engine = GameEngine()
        self._sessions: dict[UUID, dict] = {}

    def _serialize_state(self, state: GameState) -> GameSnapshot:
        return GameSnapshot(
            status=str(state.status),
            turn=state.turn,
            active_player=state.active_player,
            winner_id=state.winner_id,
            active_events=[
                GameEventState(
                    name=event.__class__.__name__,
                    duration=event.duration,
                )
                for event in state.active_events
            ],
            players={
                player_id: GamePlayerState(
                    cards_alive=len([card for card in player.board if card.is_alive()]),
                    cards=[
                        GameCardState(
                            id=card.id,
                            name=card.name,
                            health=card.health,
                            max_health=card.max_health,
                            attack=card.attack,
                            ability=str(card.ability),
                            statuses=[str(status) for status in card.statuses],
                            last_action=card.last_action,
                        )
                        for card in player.board
                    ],
                )
                for player_id, player in state.players.items()
            },
            battle_log=[
                GameLogEntry(round=entry["round"], actor=entry["actor"], text=entry["text"])
                for entry in state.battle_log
            ],
        )

    def _get_session(self, game_id: UUID) -> dict:
        session = self._sessions.get(game_id)
        if not session:
            raise HTTPException(status_code=404, detail="Game not found")
        return session

    def start_vs_bot(self) -> GameStartResponse:
        game_id = uuid4()
        player_id = uuid4()
        bot_id = uuid4()

        player = PlayerState(id=player_id)
        bot = PlayerState(id=bot_id)

        player.board.extend(draft_random_cards(player_id, count=4))
        bot.board.extend(draft_random_cards(bot_id, count=4))

        state = GameState(
            id=game_id,
            turn=0,
            active_player=player_id,
            players={player_id: player, bot_id: bot},
            status=GameStatus.ONGOING,
        )

        self._sessions[game_id] = {
            "state": state,
            "player_id": player_id,
            "bot_id": bot_id,
        }

        return GameStartResponse(
            game_id=game_id,
            player_id=player_id,
            bot_id=bot_id,
            state=self._serialize_state(state),
        )

    def _choose_bot_action(self, state: GameState, bot_id: UUID):
        bot_player = state.players[bot_id]
        alive_cards = [card for card in bot_player.board if card.is_alive()]
        if not alive_cards:
            return None, None
        chosen = alive_cards[0]
        target_id = None

        if str(chosen.ability) in ["attack"]:
            enemies = []
            for pid, player in state.players.items():
                if pid == bot_id:
                    continue
                enemies.extend([card for card in player.board if card.is_alive()])
            if enemies:
                target_id = enemies[0].id

        if str(chosen.ability) in ["heal", "buff"]:
            allies = [card for card in bot_player.board if card.is_alive()]
            if allies:
                target_id = allies[0].id

        return chosen.id, target_id

    def _append_log(self, state: GameState, round_number: int, actor: str, text: str):
        state.battle_log.append({"round": round_number, "actor": actor, "text": text})

    def play_turn(
        self, game_id: UUID, player_id: UUID, card_id: UUID, target_id: UUID | None
    ) -> GameStateResponse:
        session = self._get_session(game_id)
        state: GameState = session["state"]
        session_player_id: UUID = session["player_id"]
        bot_id: UUID = session["bot_id"]

        if player_id != session_player_id:
            raise HTTPException(status_code=403, detail="Only human player can play this turn")

        if state.status == GameStatus.FINISHED:
            return GameStateResponse(game_id=game_id, state=self._serialize_state(state))

        if state.active_player != session_player_id:
            raise HTTPException(status_code=409, detail="Not player's turn")

        round_number = state.turn + 1
        self._append_log(state, round_number, "system", f"Round {round_number} started.")
        self._engine.events_phase(state)
        if state.active_events:
            active_events_text = ", ".join(
                f"{event.__class__.__name__}({event.duration})" for event in state.active_events
            )
            self._append_log(state, round_number, "system", f"Active events: {active_events_text}")
        else:
            self._append_log(state, round_number, "system", "No active events this round.")

        for player in state.players.values():
            for card in player.board:
                card.last_action = None

        player_action_text = self._engine.play_selected_action(
            state, card_id=card_id, target_id=target_id
        )
        self._append_log(state, round_number, "player", player_action_text)

        if state.status != GameStatus.FINISHED and state.active_player == bot_id:
            bot_card_id, bot_target_id = self._choose_bot_action(state, bot_id)
            if bot_card_id is not None:
                bot_action_text = self._engine.play_selected_action(
                    state, card_id=bot_card_id, target_id=bot_target_id
                )
                self._append_log(state, round_number, "bot", bot_action_text)
            else:
                self._append_log(state, round_number, "bot", "No alive cards to act.")

        if state.status == GameStatus.FINISHED:
            if state.winner_id is None:
                self._append_log(state, round_number, "system", "Game finished in a draw.")
            elif state.winner_id == session_player_id:
                self._append_log(state, round_number, "system", "Game finished. Player wins.")
            elif state.winner_id == bot_id:
                self._append_log(state, round_number, "system", "Game finished. Bot wins.")
            else:
                self._append_log(state, round_number, "system", "Game finished.")

        state.turn = round_number

        return GameStateResponse(game_id=game_id, state=self._serialize_state(state))

    def get_state(self, game_id: UUID) -> GameStateResponse:
        session = self._get_session(game_id)
        state: GameState = session["state"]
        return GameStateResponse(game_id=game_id, state=self._serialize_state(state))


game_runtime_service = GameRuntimeService()
