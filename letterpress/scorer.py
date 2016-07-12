import sys
from queue import PriorityQueue


class Scorer(object):
    def __init__(self, board, dictionary, player):
        self.board = board
        self.dictionary = dictionary
        self.player = player
        self.defended = board.num_defended()
        self.well_defended = board.num_well_defended()
        self.found_winning_move = False
        self.moves_checked = 0
        self.lookahead_moves = 0
        self._best_moves = PriorityQueue()
        self._best_move = None

    @property
    def best_move(self):
        if not self._best_move:
            while not self._best_moves.empty():
                move = self._best_moves.get()[1]
                if self.found_winning_move or not self.opponent_can_win(move):
                    self._best_move = move
                    break
        return self._best_move

    def check_move(self, move, lookahead=True):
        self.moves_checked += 1
        new_board = self.board.capture(move, self.player)
        new_score_delta = self._get_score_delta(new_board)

        if new_board.is_full():
            if new_score_delta > 0:
                self._best_moves.put((-sys.maxsize, move))
                self.found_winning_move = True
                return
            elif new_score_delta < 0:
                # Don't kill yo self!
                return

        defended_delta = self._get_defended_delta(new_board)
        well_defended_delta = self._get_well_defended_delta(new_board)
        move_score = new_score_delta + defended_delta + well_defended_delta + len(move)

        # Priority queue uses the smallest priority
        self._best_moves.put((-move_score, move))

    def opponent_can_win(self, check_move):
        new_board = self.board.capture(check_move, self.player)
        free_letters = new_board.get_free_letters()
        free_letter_counts = {letter: free_letters.count(letter) for letter in set(free_letters)}
        index = self.dictionary.word_index
        valid_words = None
        for letter, count in free_letter_counts.items():
            words_for_letter = index[count][letter]
            if valid_words is None:
                valid_words = words_for_letter
            else:
                valid_words = valid_words.intersection(words_for_letter)

        for word in valid_words:
            for move in self.dictionary.valid_moves[word]:
                self.lookahead_moves += 1
                lookahead_board = new_board.capture(move, self.player.opponent())
                lookahead_score_delta = self._get_score_delta(lookahead_board)
                if lookahead_board.is_full() and lookahead_score_delta < 0:
                    return True
        return False

    def _get_well_defended_delta(self, new_board):
        new_well_defended = new_board.num_well_defended()
        new_well_defended_delta = (
            new_well_defended[self.player] - new_well_defended[self.player.opponent()])
        return new_well_defended_delta

    def _get_score_delta(self, new_board):
        new_score = new_board.score()
        new_score_delta = new_score[self.player] - new_score[self.player.opponent()]
        return new_score_delta

    def _get_defended_delta(self, new_board):
        new_defended = new_board.num_defended()
        new_defended_delta = new_defended[self.player] - new_defended[self.player.opponent()]
        return new_defended_delta
