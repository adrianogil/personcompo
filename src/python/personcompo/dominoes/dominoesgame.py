import random

from personcompo.framework.gameagent import GameAgent
from personcompo.framework.randombehavior import RandomBehavior

class tiles:
    TABLE = 4


class DominoesGame:
    def __init__(self):
        self.tiles = []
        self.player_tiles = []
        self.corners = []  # 0 - Up, 1 - Right, 2 - Down, 3 - Left
        self.min_tile_number = 0
        self.max_tile_number = 6
        self.number_players = 4

        self.players = []

        self.current_player = -1
        self.play_count = -1

        self.is_game_ended = False

        self.pass_on_streak = 0

        self.points = [0, 0]

    def init_game(self):
        self.is_game_ended = False

        self.generate_tiles()
        self.shuffle_tiles()
        self.define_initial_player()

        self.points = [0, 0]

    def generate_tiles(self):
        for i in range(self.min_tile_number, self.max_tile_number + 1):
            for j in range(i, self.max_tile_number + 1):
                self.tiles.append((i, j))

    def shuffle_tiles(self):
        random.shuffle(self.tiles)
        self.player_tiles = [int(i / 7) for i in range(0, 28)]

    def define_initial_player(self):
        current_tile = -1

        for i in range(0, 28):
            if self.tiles[i] == (6, 6):
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

        print("DEBUG - play_tile - player - %s - tile - %s - corner - %s - orientation - %s" % \
            (player, self.tiles[tile], corner, orientation))

        tiled_played = self.tiles[tile]

        if corner == -1 and len(self.corners) == 0 and tiled_played[0] == tiled_played[1]:
            # Initial tile
            self.corners = [tiled_played[0] for i in range(0, 4)]
        else:
            self.corners[corner] = tiled_played[(orientation + 1) % 2]

        self.pass_on_streak = 0

    def get_current_actions(self):
        current_player_tiles = [i for i in range(0, 28)
                if self.player_tiles[i] == self.current_player]

        available_actions = []

        debug_tiles = {}

        for tile in current_player_tiles:
            for corner in range(0, 4):
                for orientation in range(0, 2):
                    if self.corners[corner] == self.tiles[tile][orientation]:
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

        print("DEBUG - current_actions - player %s - hand %s\n\t%s" % (self.current_player, player_hand, debug_tiles))

        return available_actions

    def is_passed(self, action):
        return action["action"] == "pass"

    def player_passed(self, player_number):
        self.pass_on_streak += 1

    def verify_points(self):
        total_points = sum(self.corners)
        if total_points % 5 == 0:
            self.points[self.current_player % 2] += total_points

    def eval_action(self, action):
        if self.is_passed(action):
            self.player_passed(self.current_player)
        else:
            self.play_tile(self.current_player,
                           action['tile'],
                           action['corner'],
                           action['orientation'])
            self.verify_points()
        self.play_count += 1
        self.current_player = (self.current_player + 1) % 4

    def verify_end_conditions(self):
        if self.pass_on_streak >= 4:
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

    def play(self):
        self.init_game()

        while not self.is_game_ended:
            self.game_update()


game = DominoesGame()
game.players = [
    GameAgent().add_behavior("random", 1.0, RandomBehavior()),
    GameAgent().add_behavior("random", 1.0, RandomBehavior()),
    GameAgent().add_behavior("random", 1.0, RandomBehavior()),
    GameAgent().add_behavior("random", 1.0, RandomBehavior()),
]
game.play()
