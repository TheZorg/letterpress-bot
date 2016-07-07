#!/usr/bin/env python3
import sys
import os.path
import argparse
from letterpress.board import *
from letterpress.dictionary import *

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
        best_weighted_score = -sys.maxsize
        best_move = []
        current_defended = current_board.num_defended()
        current_well_defended = current_board.num_well_defended()

        for word, moves in dictionary.valid_moves.items():
            winning_word_found = False
            for move in moves:
                new_board = current_board.capture(move, player)
                new_score = new_board.score()
                new_score_delta = new_score[player] - new_score[opponent(player)]

                if new_board.is_full() and new_score_delta > 0:
                    best_move = move
                    winning_word_found = True
                    break

                new_defended = new_board.num_defended()
                defended_gained = new_defended[player] - current_defended[player]
                opponent_defended_lost = (current_defended[opponent(player)]
                                          - new_defended[opponent(player)])

                new_well_defended = new_board.num_well_defended()
                well_defended_gained = new_well_defended[player] - current_well_defended[player]
                opponent_well_defended_lost = (current_well_defended[opponent(player)]
                                          - new_well_defended[opponent(player)])

                new_weighted_score = (new_score_delta + defended_gained + opponent_defended_lost
                                      + well_defended_gained + opponent_well_defended_lost)

                if new_weighted_score > best_weighted_score:
                    best_move = move
                    best_weighted_score = new_weighted_score
                elif new_weighted_score == best_weighted_score:
                    if len(move) > len(best_move):
                        best_move = move
            if winning_word_found:
                break
        current_board = current_board.capture(best_move, player)
        word = move_to_word(best_move)
        dictionary.play_word(word)

        print('{player} played "{word}"'.format(player=player, word=word))
        print('Score is now: {score}'.format(score=current_board.score()))
        print(current_board)

        player = opponent(player)


def move_to_word(move):
    return ''.join(t.letter for t in move)


def opponent(player):
    return Player.red if player == Player.blue else Player.blue

if __name__ == '__main__':
    main()
