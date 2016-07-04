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

    print(max(d.valid_words, key=len))


def points_for_word(board, word):
    pass

if __name__ == '__main__':
    main()
