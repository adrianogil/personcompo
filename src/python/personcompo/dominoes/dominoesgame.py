import random
import sys

from personcompo.framework.gameagent import GameAgent
from personcompo.framework.randombehavior import RandomBehavior
from personcompo.dominoes.dominoesagent import GreedyDominoesBehavior

class tiles:
    TABLE = 4

# Debug print
debug_mode = False
def dprint(msg):
    if debug_mode:
        print("Debug: " + msg)

class DominoesGame:
    def __init__(self):
        self.tiles = []
        self.player_tiles = []
        self.corners = []  # 0 - Up, 1 - Right, 2 - Down, 3 - Left
        self.corners_count = [0] * 4
        self.min_tile_number = 0
        self.max_tile_number = 6
        self.number_players = 4

        self.players = []

        self.current_player = -1
        self.play_count = -1

        self.is_game_ended = False

        self.passes_in_a_row = 0
        self.last_passes_in_a_row = 0

        self.points = [0, 0]
        self.winner = -1

        self.min_points_to_win = 200

        self.games_count = 0

    def init_game(self):
        self.is_game_ended = False

        self.generate_tiles()
        self.shuffle_tiles()
        self.define_initial_player()

        self.corners_count = [0] * 4

    def generate_tiles(self):
        for i in range(self.min_tile_number, self.max_tile_number + 1):
            for j in range(i, self.max_tile_number + 1):
                self.tiles.append((i, j))

    def shuffle_tiles(self):
        random.shuffle(self.tiles)
        self.player_tiles = [int(i / 7) for i in range(0, 28)]

    def define_initial_player(self, first_game=True):
        current_tile = -1

        for i in range(0, 28):
            if (first_game and self.tiles[i] == (6, 6)) or \
                    (not first_game and self.tiles[i][0] == self.tiles[i][1]):
                current_tile = i
                self.current_player = self.player_tiles[i]
                break

        self.play_count = 1
        self.play_tile(self.current_player, current_tile, -1, 0)
        self.current_player = (self.current_player + 1) % 4

    def play_tile(self, player, tile, corner, orientation):
        '''play_tile - plays a tile[orientation] in corner
        '''
        self.player_tiles[tile] = tiles.TABLE

        dprint("DEBUG - play_tile - player - %s - tile - %s - corner - %s - orientation - %s" % \
            (player, self.tiles[tile], corner, orientation))

        tiled_played = self.tiles[tile]

        if corner == -1 and len(self.corners) == 0 and tiled_played[0] == tiled_played[1]:
            # Initial tile
            self.corners = [tiled_played[0] for i in range(0, 4)]
        else:
            self.corners[corner] = tiled_played[(orientation + 1) % 2]
            self.corners_count[corner] += 1

        self.passes_in_a_row = 0

        self.update_agents('corners', self.corners)
        self.update_agents('corners_count', self.corners_count)

    def get_current_actions(self):
        current_player_tiles = [i for i in range(0, 28)
                if self.player_tiles[i] == self.current_player]

        available_actions = []

        debug_tiles = {}

        for tile in current_player_tiles:
            for corner in range(0, 4):
                for orientation in range(0, 2):
                    if self.corners[corner] == self.tiles[tile][orientation] and \
                            (corner % 2 != 0 or self.corners_count[corner] != 0):
                        debug_key = str(self.tiles[tile])
                        if debug_key in debug_tiles:
                            debug_tiles[debug_key].append(corner)
                        else:
                            debug_tiles[debug_key] = [corner]
                        new_action = {
                            "action": "play_tile",
                            "tile": tile,
                            "tile_value": self.tiles[tile],
                            "corner": corner,
                            "orientation": orientation,
                        }
                        available_actions.append(new_action)

        if len(available_actions) == 0:
            pass_action = {
                "action": "pass"
            }
            available_actions.append(pass_action)

        player_hand = [self.tiles[i] for i in current_player_tiles]

        dprint("DEBUG - current_actions - player %s - hand %s\n\t%s" % (self.current_player, player_hand, debug_tiles))

        return available_actions

    def is_passed(self, action):
        return action["action"] == "pass"

    def player_passed(self, player_number):
        self.passes_in_a_row += 1

    def update_agents(self, world_event, world_data):
        for p in self.players:
            p.update_world_state(world_event, world_data)

    def verify_points(self, passed=False):
        if passed:
            if self.passes_in_a_row == 1:  # Last player make current player to pass
                self.points[(4 + self.current_player - 1) % 2] += 20
        else:
            if self.last_passes_in_a_row == 3:  # Galo
                self.points[self.current_player % 2] += 30

            total_points = 0

            if self.corners_count[1] >= 1 and (self.corners_count[0] + self.corners_count[2] + \
                     self.corners_count[3]) == 0:
                total_points = self.corners[1] + 2 * self.corners[0]
            elif self.corners_count[0] >= 1 and sum(self.corners_count[1:4]) == 0:
                total_points = self.corners[0] + 2 * self.corners[1]
            elif self.corners_count[0] >= 1 and self.corners_count[1] >= 1 and self.corners_count[2] >= 1:
                total_points = self.corners[0] + self.corners[1] + self.corners[2]
            elif self.corners_count[0] >= 1 and self.corners_count[1] >= 1 and self.corners_count[3] >= 1:
                total_points = self.corners[0] + self.corners[1] + self.corners[3]
            elif self.corners_count[2] >= 1 and self.corners_count[1] >= 1 and self.corners_count[3] >= 1:
                total_points = self.corners[2] + self.corners[1] + self.corners[2]
            elif self.corners_count[0] >= 1 and self.corners_count[1] >= 1 and \
                    self.corners_count[2] >= 1 and self.corners_count[3] >= 1:
                total_points = sum(self.corners)

            if total_points % 5 == 0:
                self.points[self.current_player % 2] += total_points

    def eval_action(self, action):
        if self.is_passed(action):
            self.player_passed(self.current_player)
            self.verify_points(passed=True)
        else:
            self.play_tile(self.current_player,
                           action['tile'],
                           action['corner'],
                           action['orientation'])
            self.verify_points()
        self.play_count += 1
        self.current_player = (self.current_player + 1) % 4

    def verify_end_conditions(self):
        if self.passes_in_a_row >= 4:
            return True

        for player in range(0, 4):
            total_tiles = 0
            for t in range(0, 28):
                if self.player_tiles[t] == player:
                    total_tiles += 1
            if total_tiles == 0:
                return True

        return False

    def game_update(self):
        possible_actions = self.get_current_actions()
        current_action = self.players[self.current_player].get_action(possible_actions)
        self.eval_action(current_action)
        if self.verify_end_conditions():
            self.is_game_ended = True

    def verify_winner(self):

        if self.points[0] == self.points[1]:
            self.winner = -1
        elif self.points[0] > self.points[1]:
            self.winner = 0
        else:
            self.winner = 1

        if self.winner == -1:
            print("Result: Draw")
        else:
            print("Team %s wins! %s" % ("A" if self.winner == 0 else "B", self.points))

    def play(self):
        self.games_count = 0
        self.points = [0, 0]

        while max(self.points) < self.min_points_to_win:
            self.init_game()

            while not self.is_game_ended:
                self.game_update()

        self.verify_winner()


number_of_games = 1


if len(sys.argv) == 2:
    if sys.argv[1] == '-d' or sys.argv[1] == '--details':
        debug_mode = True
    else:
        number_of_games = int(sys.argv[1])

winner_stats = [0, 0, 0]


def get_teamA_agent():
    return GameAgent()\
        .add_behavior("greedy", 1.0, GreedyDominoesBehavior())


def get_teamB_agent():
    return GameAgent()\
        .add_behavior("random", 1.0, RandomBehavior())


for i in range(0, number_of_games):
    game = DominoesGame()
    game.players = [
       get_teamA_agent(),
       get_teamB_agent(),
       get_teamA_agent(),
       get_teamB_agent()
    ]
    game.play()
    winner_stats[game.winner+1] += 1

print("Game stats: %s" % (winner_stats))
