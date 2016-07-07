import copy
from collections import namedtuple
from enum import Enum
from termcolor import colored

Position = namedtuple('Position', ['x', 'y'])


class Player(Enum):
    blue = 1
    red = 2


class Tile(namedtuple('Tile', 'x y letter')):
    __slots__ = ()

    def __str__(self):
        return self.letter

    def __repr__(self):
        return '{letter}@{{{x}, {y}}}'.format(letter=self.letter, x=self.x, y=self.y)


class Board(object):
    SIZE = 5

    def __init__(self, layout):
        """
        Create a new blank board from the give layout.
        :type layout_file: TextIOBase
        :param layout_file: A file containing a grid of letters, with columns separated by spaces
                and rows by newlines.
        """
        self._tiles = [[Tile(x, y, letter) for x, letter in enumerate(row.lower().split())]
                       for y, row in enumerate(layout)]
        self._ownership = {tile: None for row in self._tiles for tile in row}
        self._defended_cache = {}

    @property
    def tiles(self):
        """
        Get the board as a matrix of Tiles.
        """
        return self._tiles

    def capture(self, move, player):
        """
        Capture a sequence of tiles for the given player. Returns a modified Board instance.
        :param move: Iterable of tile position pairs (x, y).
        :param player: The player capturing the tiles.
        :return: Copy of Board, with tiles captured
        """
        ret = self.copy()
        for tile in move:
            if not self._is_defended(tile):
                ret._take_tile(tile, player)
        return ret

    def score(self):
        """
        Get the current score for the board
        :return: {Player.blue: score, Player.red: score}
        """
        return {player: sum(v == player for v in self._ownership.values()) for player in Player}

    def num_defended(self):
        ret = {p: 0 for p in Player}
        for tile, player in self._ownership.items():
            if player:
                ret[player] += self._is_defended(tile)
        return ret

    def num_well_defended(self):
        ret = {p: 0 for p in Player}
        for tile, player in self._ownership.items():
            if player:
                ret[player] += self._is_well_defended(tile)
        return ret

    def is_full(self):
        return all(self._ownership.values())

    def get_valid_letters(self):
        valid_letters = {}
        for line in self._tiles:
            for tile in line:
                if tile.letter in valid_letters:
                    valid_letters[tile.letter] += 1
                else:
                    valid_letters[tile.letter] = 1
        return valid_letters

    def copy(self):
        ret = copy.copy(self)
        ret._ownership = self._ownership.copy()
        ret._defended_cache = {}
        return ret

    def _get_tile(self, tile_x, tile_y):
        x_in_bounds = 0 <= tile_x < Board.SIZE
        y_in_bounds = 0 <= tile_y < Board.SIZE
        if x_in_bounds and y_in_bounds:
            return self._tiles[tile_y][tile_x]
        else:
            return None

    def _take_tile(self, tile, player):
        self._ownership[tile] = player

    def _is_defended(self, tile):
        player = self._ownership[tile]
        if not player:
            # Uncaptured tiles cannot be defended
            return False

        if tile in self._defended_cache:
            return self._defended_cache[tile]

        is_defended = True
        surrounding = [(tile.x, tile.y - 1), (tile.x, tile.y + 1),
                       (tile.x - 1, tile.y), (tile.x + 1, tile.y)]
        for neighbor_x, neighbor_y in surrounding:
            neighbor = self._get_tile(neighbor_x, neighbor_y)
            if neighbor and self._ownership[neighbor] != player:
                is_defended = False
                break

        self._defended_cache[tile] = is_defended

        return is_defended

    def _is_well_defended(self, tile):
        player = self._ownership[tile]
        if not player:
            # Uncaptured tiles cannot be defended
            return False

        if not self._is_defended(tile):
            return False

        surrounding = [(tile.x, tile.y - 1), (tile.x, tile.y + 1),
                       (tile.x - 1, tile.y), (tile.x + 1, tile.y)]

        for x, y in surrounding:
            neighbor = self._get_tile(x, y)
            if neighbor and (self._ownership[neighbor] != player or not self._is_defended(neighbor)):
                return False
        return True

    color_for = {
        Player.blue: 'blue',
        Player.red: 'red',
    }

    def _get_color_for(self, player):
        return self.color_for.get(player, None)

    def __str__(self):
        grid = []
        for row in self._tiles:
            print_row = []
            for tile in row:
                colors = {'color': None, 'on_color': None}
                color = self._get_color_for(self._ownership[tile])
                if self._is_defended(tile):
                    colors['on_color'] = 'on_' + color
                    colors['color'] = 'white'
                else:
                    colors['color'] = color
                print_row.append(colored(tile.letter.upper(), **colors))
            grid.append(" ".join(print_row))
        return "\n".join(grid)
