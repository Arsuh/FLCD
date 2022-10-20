import re
from hashTable import HashTable

EXERCISE_PATH = './Exercises/ex1.txt'
TOKEN_PATH = './Token.txt'

class Parser:
    def __init__(self, exercise_path=EXERCISE_PATH, token_path=TOKEN_PATH):
        self.exercise_path = exercise_path
        self.token_path = token_path

        self.token_list = []
        self.reserved_tokens = []
        self.operators_regex = ''
        self.hash_table = HashTable()

    def parse(self):
        self._load_exercise()
        self._load_reserved_tokens()
        self._build_hash_table()

    def _load_exercise(self):
        with open(self.exercise_path, 'r', encoding='utf-8') as f:
            text = f.read()

        tokens = re.split('( |\n|\t|\(|\)|\{|\}|\[|\]|&|\||<=|>=|==)', text)    # split by space, new line, tab any paranthesis or <=, >=, ==
        tokens = list(filter(('').__ne__, tokens))
        tokens = list(filter((' ').__ne__, tokens))
        tokens = list(filter(('\n').__ne__, tokens))
        self.token_list = list(filter(('\t').__ne__, tokens))

    def _load_reserved_tokens(self):
        with open(self.token_path, 'r', encoding='utf-8') as f:
            self.reserved_tokens = f.read().split('\n')


    def _build_hash_table(self):
        for token in self.token_list:
            if token not in self.reserved_tokens:
                self.hash_table.add(token)


if __name__ == '__main__':
    parser = Parser()
    parser.parse()
    print(parser.token_list)
    print(parser.hash_table)