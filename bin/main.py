#!/usr/bin/env python3
import sys
import os.path
import argparse
from timeit import default_timer
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from letterpress.board import *
from letterpress.dictionary import *
from letterpress.scorer import *


def main():
    parser = argparse.ArgumentParser(description='Letterpress bot.')
    parser.add_argument('--board', '-b', required=True,
                        type=argparse.FileType('r'))
    parser.add_argument('--dict', '-d', required=True,
                        type=argparse.FileType('r'))

    args = parser.parse_args()
    dict_file = args.dict
    board_file = args.board
    board = Board(board_file.readlines())
    dictionary = Dictionary(dict_file, board)

    print("Initialization done, starting game.")
    player = Player.blue
    print("Player {player} is up.".format(player=player.name))
    current_board = board
    timer = default_timer
    while not current_board.is_full():
        start_time = timer()
        scorer = Scorer(current_board, dictionary, player)

        for move in (move for moves in dictionary.valid_moves.values() for move in moves):
            scorer.check_move(move)
            if scorer.found_winning_move:
                break

        if not scorer.best_move:
            print('The only winning move is not to play...')
        else:
            current_board = current_board.capture(scorer.best_move, player)
            word = move_to_word(scorer.best_move)
            dictionary.play_word(word)
            print('{player} played "{word}"'.format(player=player, word=word))
        end_time = timer()

        print('moves checked: {moves}, lookahead: {lookahead}'
              .format(moves=scorer.moves_checked,lookahead=scorer.lookahead_moves))
        print('Score is now: {score}'.format(score=current_board.score()))
        print('Took {time:.2f}s'.format(time=end_time - start_time))
        print(current_board)

        player = player.opponent()

    final_score = current_board.score()
    winner = max(final_score, key=final_score.get)
    print("Player {player} wins the game! Final score: {score}".format(player=winner, score=final_score))



def move_to_word(move):
    return ''.join(t.letter for t in move)


if __name__ == '__main__':
    main()
