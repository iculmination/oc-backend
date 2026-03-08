class GameEngine:

    def apply_action(self, state, action):

        if action["type"] == "play_card":
            return self.play_card(state, action)

        if action["type"] == "attack":
            return self.attack(state, action)

        if action["type"] == "end_turn":
            return self.end_turn(state)

    def play_card(self, state, action):

        player = state.players[action["player_id"]]

        card_id = action["card_id"]

        card = next(c for c in player.hand if str(c.id) == card_id)

        player.hand.remove(card)
        player.board.append(card)

    def attack(self, state, action):

        attacker = self.find_card(state, action["attacker"])
        defender = self.find_card(state, action["defender"])

        defender.health -= attacker.attack
        attacker.health -= defender.attack

    def end_turn(self, state):

        state.turn += 1

        players = list(state.players.keys())

        current = players.index(state.active_player)

        state.active_player = players[(current + 1) % len(players)]

    def find_card(self, state, card_id):

        for player in state.players.values():

            for card in player.board:

                if str(card.id) == card_id:
                    return card

        return None
