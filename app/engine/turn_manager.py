import random


class TurnManager:

    def process_turn(self, state):

        if random.random() < 0.25:
            self.spawn_random_event(state)

    def spawn_random_event(self, state):

        event = {"type": "blood_rain", "duration": 3}  # TODO: implement event spawning

        state.active_events.append(event)
