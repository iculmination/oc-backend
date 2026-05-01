import random


def get_random_enemy(state, player_id):
    enemies = []
    for pid, player in state.players.items():
        if pid == player_id:
            continue
        enemies.extend(player.board)
    return random.choice(enemies) if enemies else None


def get_random_ally(state, player_id):
    player = state.players[player_id]
    return random.choice(player.board) if player.board else None


def get_enemy_by_id(state, player_id, target_id):
    for pid, player in state.players.items():
        if pid == player_id:
            continue
        for card in player.board:
            if str(card.id) == str(target_id):
                return card
    return None


def get_ally_by_id(state, player_id, target_id):
    player = state.players[player_id]
    for card in player.board:
        if str(card.id) == str(target_id):
            return card
    return None
