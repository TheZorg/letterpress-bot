from collections import defaultdict

class Dictionary():
    def __init__(self, dict_file, board):
        """
        Create a new dictionary containing all the words in dict_file that could be played on the
        board.
        :param dict_file: A newline-delimited file of words.
        """
        self._make_valid_words(dict_file, board)
        self._make_valid_moves(board)

    def play_word(self, word):
        for i in range(len(word)):
            prefix = word[0:i + 1]
            if prefix in self.valid_words:
                self.valid_words.remove(prefix)
            if prefix in self.valid_moves:
                del self.valid_moves[prefix]

    def _make_valid_words(self, dict, board):
        print("Dictionary: computing valid words...")
        valid_words = set()
        valid_letters = board.get_valid_letters()
        for word in dict:
            word = word.strip()
            letters = valid_letters.copy()
            valid = True
            for c in word.lower():
                if c in letters and letters[c] > 0:
                    letters[c] -= 1
                else:
                    valid = False
                    break
            if valid and word:
                valid_words.add(word)

        self.valid_words = valid_words

    def _make_valid_moves(self, board):
        print("Dictionary: computing valid moves...")
        tile_map = defaultdict(list)
        for row in board.tiles:
            for tile in row:
                tile_map[tile.letter].append(tile)

        valid_moves = {}
        for word in self.valid_words:
            moves = []
            self._add_all_init(word, moves, tile_map)
            valid_moves[word] = moves

        self.valid_moves = valid_moves

    def _add_all_init(self, word, moves, tile_map):
        first, *rest = word
        self._add_all(first, rest, (), moves, tile_map)

    def _add_all(self, letter, rest, move, moves, tile_map):
        if not rest:
            for tile in tile_map[letter]:
                moves.append(move + (tile,))
        else:
            next, *next_rest = rest
            tile_map_copy = tile_map.copy()
            tile_map_copy[letter] = tile_map_copy[letter].copy()
            for tile in tile_map[letter]:
                tile_map_copy[letter].remove(tile)
                next_move = move + (tile,)
                self._add_all(next, next_rest, next_move, moves, tile_map_copy)
