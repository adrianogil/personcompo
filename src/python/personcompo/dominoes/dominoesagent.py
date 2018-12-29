from copy import deepcopy


class GreedyDominoesBehavior:
    def __init__(self):
        pass

    def update_world_state(self, world_state):
        return world_state

    def eval(self, action, world_state):
        if action['action'] != 'play_tile':
            return -1

        corners = deepcopy(world_state['corners'])
        corners_count = world_state['corners_count']

        next_points = 0

        # Get points for tile
        tile = action['tile_value']
        target_corner = action['corner']
        target_orientation = action['orientation']

        corners[target_corner] = tile[(target_orientation + 1) % 2]

        if corners_count[1] >= 1 and sum([corners_count[0]] + corners_count[2:4]) == 0:
            next_points = corners[1] + 2 * corners[0]
        elif corners_count[0] >= 1 and sum(corners_count[1:4]) == 0:
            next_points = corners[0] + 2 * corners[1]
        elif corners_count[0] >= 1 and corners_count[1] >= 1 and corners_count[2] >= 1:
            next_points = corners[0] + corners[1] + corners[2]
        elif corners_count[0] >= 1 and corners_count[1] >= 1 and corners_count[3] >= 1:
            next_points = corners[0] + corners[1] + corners[3]
        elif corners_count[2] >= 1 and corners_count[1] >= 1 and corners_count[3] >= 1:
            next_points = corners[2] + corners[1] + corners[2]
        elif corners_count[0] >= 1 and corners_count[1] >= 1 and \
                corners_count[2] >= 1 and corners_count[3] >= 1:
            next_points = sum(corners)
        if next_points % 5 != 0:
            next_points = 0

        return next_points
