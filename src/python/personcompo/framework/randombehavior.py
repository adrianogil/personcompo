import random


class RandomBehavior:
    def __init__(self):
        pass

    def eval(self, action):
        return random.uniform(0.0, 100.0)
