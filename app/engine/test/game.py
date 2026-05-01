from uuid import uuid4

from loguru import logger

from app.engine.game_engine import GameEngine
from app.engine.state.game import GameState
from app.engine.state.player import PlayerState

from app.engine.mock.cards import soldier, medic, void_beast

from app.enums.game import GameStatus


def test_game_engine():
    player1 = uuid4()
    player2 = uuid4()

    p1 = PlayerState(id=player1)
    p2 = PlayerState(id=player2)

    p1.board.append(soldier(player1))
    p1.board.append(medic(player1))

    p2.board.append(void_beast(player2))

    state = GameState(
        id=uuid4(), turn=1, active_player=player1, players={player1: p1, player2: p2}
    )

    engine = GameEngine()

    for i in range(5):
        current_state = engine.process_turn(state)
        if current_state.status == GameStatus.FINISHED:
            logger.info("The game is over")
            break

    return {
        "status": state.status,
        "winner_id": str(state.winner_id) if state.winner_id else None,
        "turn": state.turn,
        "active_player": str(state.active_player),
        "active_events": len(state.active_events),
        "players": {
            str(player_id): {
                "cards_alive": len([card for card in player.board if card.is_alive()]),
                "cards": [
                    {
                        "name": card.name,
                        "health": card.health,
                        "statuses": [str(status) for status in card.statuses],
                    }
                    for card in player.board
                ],
            }
            for player_id, player in state.players.items()
        },
    }
