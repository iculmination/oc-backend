from uuid import uuid4

from app.engine.game_engine import GameEngine
from app.engine.state.game import GameState
from app.engine.state.player import PlayerState

from app.engine.mock.cards import soldier, medic, void_beast


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

        engine.process_turn(state)

        for player in state.players.values():

            for card in player.board:
                pass  # TODO: remove this
