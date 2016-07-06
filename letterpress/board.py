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
        return {Player.blue: sum(v == Player.blue for v in self._ownership.values()),
                Player.red: sum(v == Player.red for v in self._ownership.values())}

    def num_defended(self):
        return {Player.blue: sum(p == Player.blue and self._is_defended(t)
                                for t, p in self._ownership.items()),
                Player.red: sum(p == Player.red and self._is_defended(t)
                                 for t, p in self._ownership.items())}

    def num_well_defended(self):
        return {Player.blue: sum(p == Player.blue and self._is_well_defended(t)
                                 for t, p in self._ownership.items()),
                Player.red: sum(p == Player.red and self._is_well_defended(t)
                                for t, p in self._ownership.items())}

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
        return ret

    def _get_tile(self, x, y):
        x_in_bounds = 0 <= x < Board.SIZE
        y_in_bounds = 0 <= y < Board.SIZE
        if x_in_bounds and y_in_bounds:
            return self._tiles[y][x]
        else:
            return None

    def _take_tile(self, tile, player):
        self._ownership[tile] = player

    def _is_defended(self, tile):
        player = self._ownership[tile]
        if not player:
            # Uncaptured tiles cannot be defended
            return False

        surrounding = [(tile.x, tile.y - 1), (tile.x, tile.y + 1),
                       (tile.x - 1, tile.y), (tile.x + 1, tile.y)]
        for x, y in surrounding:
            neighbor = self._get_tile(x, y)
            if neighbor and self._ownership[neighbor] != player:
                return False
        return True

    def _is_well_defended(self, tile):
        player = self._ownership[tile]
        if not player:
            # Uncaptured tiles cannot be defended
            return False

        defended = [[self._is_defended(tile) and self._ownership[tile] == player for tile in row]
                    for row in self._tiles]

        surrounding = [(tile.x, tile.y - 1), (tile.x, tile.y + 1),
                       (tile.x - 1, tile.y), (tile.x + 1, tile.y)]
        for x, y in surrounding:
            defended_neighbor = not 0 <= x < Board.SIZE or not 0 <= y < Board.SIZE or defended[y][x]
            if not defended_neighbor:
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
