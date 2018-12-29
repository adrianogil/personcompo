import random


class RandomBehavior:
    def __init__(self):
        pass

    def update_world_state(self, world_state):
        return world_state

    def eval(self, action, world_state):
        return random.uniform(0.0, 100.0)
