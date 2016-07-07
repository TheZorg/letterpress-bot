import sys


class Scorer(object):
    def __init__(self, board, dictionary, player):
        self.board = board
        self.dictionary = dictionary
        self.player = player
        self.best_move = []
        self.best_weighted_score = -sys.maxsize
        self.defended = board.num_defended()
        self.well_defended = board.num_well_defended()
        self.found_winning_move = False

    def check_move(self, move):
        new_board = self.board.capture(move, self.player)
        new_score_delta = self._get_score_delta(new_board)

        if new_board.is_full() and new_score_delta > 0:
            self.best_move = move
            self.found_winning_move = True
            return

        new_defended_delta = self._get_defended_delta(new_board)
        new_well_defended_delta = self._get_well_defended_delta(new_board)
        new_weighted_score = new_score_delta + new_defended_delta + new_well_defended_delta

        if new_weighted_score > self.best_weighted_score:
            self.best_move = move
            self.best_weighted_score = new_weighted_score
        elif new_weighted_score == self.best_weighted_score:
            # Always play the longer word
            if len(move) > len(self.best_move):
                self.best_move = move

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
