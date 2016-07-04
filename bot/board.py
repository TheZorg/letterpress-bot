from collections import namedtuple
from enum import Enum
from termcolor import colored

Position = namedtuple('Position', ['x', 'y'])


class Player(Enum):
    blue = 1
    red = 2


class Tile:
    def __init__(self, x, y, letter, owned_by):
        self.x = x
        self.y = y
        self.letter = letter
        self.owned_by = owned_by

    def __str__(self):
        return self.letter


class Board:
    SIZE = 5

    def __init__(self, layout_file):
        """
        Create a new blank board from the give layout.
        :type layout_file: TextIOBase
        :param layout_file: A file containing a grid of letters, with columns separated by spaces
                and rows by newlines.
        """
        self._layout = [[Tile(x, y, letter, None) for x, letter in enumerate(row.lower().split())]
                        for y, row in enumerate(layout_file)]
        self._valid_letters = self._make_valid_letters()

    @property
    def valid_letters(self):
        """
        Get a dict of valid letters and the associated count for each of them.
        """
        return self._valid_letters.copy()

    def capture(self, move, player):
        for pos in move:
            target = self._get_tile(*pos)
            target.owned_by = player
        return self


    def current_score(self):
        score = {Player.blue: 0, Player.red: 0}
        for row in self._layout:
            for tile in row:
                if tile.owned_by:
                    score[tile.owned_by] += 1
        return score

    def _make_valid_letters(self):
        valid_letters = {}
        for line in self._layout:
            for tile in line:
                if tile.letter in valid_letters:
                    valid_letters[tile.letter] += 1
                else:
                    valid_letters[tile.letter] = 1
        return valid_letters

    def _get_tile(self, x, y):
        x_in_bounds = 0 <= x < Board.SIZE
        y_in_bounds = 0 <= y < Board.SIZE
        if x_in_bounds and y_in_bounds:
            return self._layout[y][x]
        else:
            return None

    def _is_defended(self, tile):
        player = tile.owned_by
        if not player:
            # Uncaptured tiles cannot be defended
            return False

        surrounding = [(tile.x, tile.y - 1), (tile.x, tile.y + 1),
                       (tile.x - 1, tile.y), (tile.x + 1, tile.y)]
        for each in surrounding:
            neighbor = self._get_tile(*each)
            if neighbor and neighbor.owned_by != player:
                return False
        return True

    color_for = {
        Player.blue: 'blue',
        Player.red: 'red',
    }

    def _get_color_for(self, player):
        return self.color_for.get(player, 'grey')

    def __str__(self):
        grid = []
        for row in self._layout:
            print_row = []
            for tile in row:
                attrs = ['bold'] if self._is_defended(tile) else []
                color = self._get_color_for(tile.owned_by)
                print_row.append(colored(tile.letter.upper(), color, attrs=attrs))
            grid.append(" ".join(print_row))
        return "\n".join(grid)
