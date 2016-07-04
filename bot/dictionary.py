class Dictionary():
    def __init__(self, dict_file, board):
        """
        Create a new dictionary containing all the words in dict_file that could be played on the
        board.
        :param dict_file: A newline-delimited file of words.
        """
        self.valid_words = Dictionary._make_valid_words(dict_file, board)

    @staticmethod
    def _make_valid_words(dict, board):
        valid_words = set()
        for word in dict:
            word = word.strip()
            letters = board.valid_letters
            valid = True
            for c in word.lower():
                if c in letters and letters[c] > 0:
                    letters[c] -= 1
                else:
                    valid = False
                    break
            if valid and word:
                valid_words.add(word)
        return valid_words
