import re
from hashTable import HashTable, LinkedList, Node
from finiteAutomata import FA

EXERCISE_PATH = './Exercises/ex1.txt'
TOKEN_PATH = './Token.txt'

CONSTANT = '0_CONST'
IDENTIFIER = '1_IDENTIFIER'

class Parser:
    def __init__(self, token_path=TOKEN_PATH):
        self.token_path = token_path

        self.token_table = {}
        self.reserved_tokens = []
        self.symbol_table = HashTable()
        self.pif = LinkedList()

        self.fa_identifier = FA(fa_path='./FiniteAutomata/FA_identifier.in')
        self.fa_integer = FA(fa_path='./FiniteAutomata/FA_integer_constant.in')

        self.st_out = './ST.out'
        self.pif_out = './PIF.out'

    def parse(self, exercise_path):
        self._load_reserved_tokens()

        try:
            self._load_exercise(exercise_path)

            with open(self.st_out, 'w', encoding='utf-8') as f:
                f.write(f'Symbol table - hash table\n{self.symbol_table}')

            with open(self.pif_out, 'w', encoding='utf-8') as f:
                f.write(str(self.pif))

            print('Lexically correct!')

        except Exception as e:
            with open(self.st_out, 'w', encoding='utf-8') as f:
                f.write(str(e))

            with open(self.pif_out, 'w', encoding='utf-8') as f:
                f.write(str(e))

            print(e)

    def _load_exercise(self, exercise_path):
        with open(exercise_path, 'r', encoding='utf-8') as f:
            text = f.read().split('\n')

        for line_number, line in enumerate(text):
            tokens = re.split('( |\n|\t|\(|\)|\{|\}|\[|\]|&|\||<=|>=|==)', line)
            tokens = list(filter((' ').__ne__, tokens))
            tokens = list(filter(('').__ne__, tokens))

            self._create_pif(tokens, line_number)

    def _create_pif(self, tokens, line_number):
        for token in tokens:
            # check if token is a reserved word OR operator OR separator
            if token in self.token_table:
                self.pif.add(Node((token, self.token_table[token], -1)))

            else:
                # if token is not in the symbol table, add it
                if token not in self.reserved_tokens:
                    self.symbol_table.add(token)

                # check if token is an identifier
                #if re.match(r'^[a-zA-z]\w*$', token):
                if self.fa_identifier.check(token):
                    self.pif.add(Node((token, self.token_table[IDENTIFIER], self.symbol_table[token].data[1])))

                # check if token is an integer constant
                elif self.fa_integer.check(token):
                    self.pif.add(Node((token, self.token_table[CONSTANT], self.symbol_table[token].data[1])))

                # check if token is a string constant
                #elif re.match(r"^'.*'$|^-*[0-9]+$", token):
                elif re.match(r"^'.*'$", token):
                    self.pif.add(Node((token, self.token_table[CONSTANT], self.symbol_table[token].data[1])))
                
                else:
                    raise Exception(f'Lexical error at line {line_number + 1} | Token: {token}!')

    def _load_reserved_tokens(self):
        with open(self.token_path, 'r', encoding='utf-8') as f:
            self.reserved_tokens = f.read().split('\n')

        self.token_table[CONSTANT] = 0
        self.token_table[IDENTIFIER] = 1

        i = 2
        for token in self.reserved_tokens[1:]:
            self.token_table[token] = i
            i += 1


if __name__ == '__main__':
    p = Parser()
    p.parse(exercise_path=EXERCISE_PATH)