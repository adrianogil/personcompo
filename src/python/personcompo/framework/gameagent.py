
class GameAgent:
    def __init__(self):
        self.behaviors = {}

    def add_behavior(self, name, weight, behavior):
        self.behaviors[name] = {
            "weight": weight,
            "object": behavior
        }

        return self

    def assess_action(self, action):
        utility_value = 0

        for behavior in self.behaviors:
            utility_value += self.behaviors[behavior]["weight"] * self.behaviors[behavior]["object"].eval(action)

        return utility_value

    def get_action(self, actions):
        best_action = None
        best_utility_value = 1000000

        for action in actions:
            u = self.assess_action(action)
            if u < best_utility_value:
                best_utility_value = u
                best_action = action

        return best_action
