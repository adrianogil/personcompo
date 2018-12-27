import random


class DominoesGame:
    def __init__(self):
        self.tiles = []
        self.player_tiles = []
        self.min_tile_number = 0
        self.max_tile_number = 6
        self.number_players = 4

        self.current_player = -1

    def init_game(self):
        self.generate_tiles()
        self.shuffle_tiles()
        self.define_initial_player()

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

        self.play_tile(self.current_player, current_tile)

    def play_tile(self, player, tile):
        pass

    def play(self):
        self.init_game()


game = DominoesGame()
game.play()
