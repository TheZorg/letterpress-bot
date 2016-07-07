#!/usr/bin/env python3
import sys
import os.path
import argparse
import time
from letterpress.board import *
from letterpress.dictionary import *
from letterpress.scorer import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def main():
    parser = argparse.ArgumentParser(description='Letterpress bot.')
    parser.add_argument('--board', '-b', required=True,
                        type=argparse.FileType('r', encoding='ascii'))
    parser.add_argument('--dict', '-d', required=True,
                        type=argparse.FileType('r', encoding='ascii'))

    args = parser.parse_args()
    dict_file = args.dict
    board_file = args.board
    board = Board(board_file.readlines())
    dictionary = Dictionary(dict_file, board)

    print("Initialization done, starting game.")
    player = Player.blue
    print("{player} is up.".format(player=player))
    current_board = board
    while not current_board.is_full():
        start_time = time.perf_counter()
        scorer = Scorer(current_board, dictionary, player)

        for move in (move for moves in dictionary.valid_moves.values() for move in moves):
            scorer.check_move(move)
            if scorer.found_winning_move:
                break

        current_board = current_board.capture(scorer.best_move, player)
        word = move_to_word(scorer.best_move)
        dictionary.play_word(word)
        end_time = time.perf_counter()

        print('{player} played "{word}"'.format(player=player, word=word))
        print('Score is now: {score}'.format(score=current_board.score()))
        print('Took {time:.2f}s'.format(time=end_time - start_time))
        print(current_board)

        player = player.opponent()


def move_to_word(move):
    return ''.join(t.letter for t in move)


if __name__ == '__main__':
    main()
