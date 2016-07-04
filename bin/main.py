import argparse
from bot.board import *
from bot.dictionary import *

def main():
    parser = argparse.ArgumentParser(description='Letterpress bot.')
    parser.add_argument('--board', '-b', required=True,
                        type=argparse.FileType('r', encoding='ascii'))
    parser.add_argument('--dict', '-d', required=True,
                        type=argparse.FileType('r', encoding='ascii'))

    args = parser.parse_args()
    dict_file = args.dict
    board_file = args.board
    b = Board(board_file)
    d = Dictionary(dict_file, b)


    b.capture([(0, 0), (0, 1), (1, 0)], Player.blue)
    print(b)

    biggest_word = max(d.valid_words, key=len)
    print(biggest_word)
    print(d.valid_moves[biggest_word])

    total_moves = 0
    total_words = 0
    for word, moves in d.valid_moves.items():
        total_words += 1
        total_moves += len(moves)

    print(total_words)
    print(total_moves)


def points_for_word(board, word):
    pass

if __name__ == '__main__':
    main()
