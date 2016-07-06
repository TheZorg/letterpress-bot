#!/usr/bin/env python3

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import argparse
from letterpress.board import *
from letterpress.dictionary import *

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

    player = Player.blue
    current_board = board
    while not current_board.is_full():
        best_score_delta = -sys.maxsize
        best_word = ''
        best_move = []

        player = opponent(player)

        for word, moves in dictionary.valid_moves.items():
            winning_word_found = False
            for move in moves:
                new_board = current_board.capture(move, player)
                new_score = new_board.score()
                new_score_delta = new_score[player] - new_score[opponent(player)]
                if new_board.is_full() and new_score_delta > 0:
                    best_word = word
                    best_move = move
                    winning_word_found = True
                    break
                if new_score_delta > best_score_delta:
                    best_word = word
                    best_move = move
                    best_score_delta = new_score_delta
                elif new_score_delta == best_score_delta:
                    if len(word) > len(best_word):
                        best_word = word
                        best_move = move
            if winning_word_found:
                break
        current_board = current_board.capture(best_move, player)
        dictionary.play_word(best_word)
        print('{player} played "{word}"'.format(player=player, word=best_word))
        print('Score is now: {score}'.format(score=current_board.score()))
        print(current_board)

def opponent(player):
    return Player.red if player == Player.blue else Player.blue

if __name__ == '__main__':
    main()
