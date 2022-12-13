from pprint import pprint

FILE = './Grammars/g4.txt'

class Grammar:
    EPSILON = 'EPSILON'
    EPMTY = '$'
    ERROR = None
    POP = 'POP'
    ACC = 'ACC'

    def __init__(self, file):
        self.file = file

        self.nonterminals = []
        self.terminals = []
        self.start = None
        self.productions = {}

        self.first_table = {}
        self.follow_table = {}

    def read(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')

        self.nonterminals = lines[0].split(' ')
        self.terminals = lines[1].split(' ')
        self.start = lines[2]

        for line in lines[3:]:
            main, prods = line.split(' -> ')

            if main not in self.productions:
                self.productions[main] = []

            for prod in prods.split(' | '):
                self.productions[main].append(prod)

    def productions_for_nonterminal(self, nonterminal):
        res = []

        for key, prods in self.productions.items():
            for prod in prods:
                if nonterminal in prod.split(' '):
                    res.append(f'{key} -> {prod}')

        res.append(f'{nonterminal} -> {self.productions[nonterminal]}')

        return res

    def check(self):
        for key in self.productions:
            if key not in self.nonterminals:
                return False

        return True

    def first_follow(self):
        for nonterminal in self.nonterminals:
            self.first_table[nonterminal] = self.first(nonterminal)
        
        for nonterminal in self.nonterminals:
            self.follow_table[nonterminal] = self.follow(nonterminal)

    def first(self, nonterminal):
        first_set = set()

        for production in self.productions[nonterminal]:
            elements = production.split(' -> ')[-1].split(' ')
            _first = elements[0]

            if _first == nonterminal:
                continue

            if _first in self.terminals:
                first_set.add(_first)

            elif _first in self.nonterminals:
                for elem in elements:
                    if elem in self.nonterminals:
                        returned_first_set = self.first(elem)

                        for elem in returned_first_set:
                            first_set.add(elem)

                        if Grammar.EPSILON not in returned_first_set:
                            break
                    else:
                        first_set.add(elem)
                        break

            else:
                raise Exception('Incorrect grammar!')

        return first_set


    def follow(self, nonterminal):
        follow_set = set()

        if nonterminal == self.start:
            follow_set.add(Grammar.EPMTY)
            

        for name, production in self.productions.items():
            for elem in production:

                elements = elem.split(' ')
                if nonterminal in elements:
                    index = elements.index(nonterminal)

                    if index == len(elements) - 1:
                        if nonterminal != name:
                            returned_follow_set = self.follow(name)

                            for elem in returned_follow_set:
                                follow_set.add(elem)

                    elif elements[index + 1] in self.terminals:
                        follow_set.add(elements[index + 1])

                    elif elements[index + 1] in self.nonterminals:
                        for i in range(index + 1, len(elements)):
                            if elements[i] in self.terminals:
                                follow_set.add(elements[i])
                                break

                            _first = self.first_table[elements[i]]

                            for f in _first:
                                if f != Grammar.EPSILON:
                                    follow_set.add(f)

                            if i == len(elements) - 1 and Grammar.EPSILON in _first:
                                returned_follow_set = self.follow(name)

                                for elem in returned_follow_set:
                                    follow_set.add(elem)

                            if Grammar.EPSILON not in _first:
                                break

                    else:
                        raise Exception('Incorrect grammar!')

        return follow_set

    def _init_ll1_table(self):
        self.table = [[None for _ in range(len(self.terminals) + 1)] for _ in range(len(self.nonterminals) + len(self.terminals) + 1)]
        
        for i in range(len(self.terminals)):
            self.table[0][i+1] = self.terminals[i]

        for i in range(len(self.nonterminals)):
            self.table[i+1][0] = self.nonterminals[i]

        j = 1
        for i in range(len(self.nonterminals) + 1, len(self.nonterminals) + len(self.terminals) + 1):
            self.table[i][0] = self.terminals[i - len(self.nonterminals) - 1]

            self.table[i][j] = Grammar.POP
            j += 1
            
        self.table[-1][-1] = Grammar.ACC

    def get_move(self, x, y):
        idx_x, idx_y = None, None

        for i in range(1, len(self.terminals) + len(self.nonterminals) + 1):
            if self.table[i][0] == x:
                idx_x = i
                break

        for i in range(1, len(self.terminals) + 1):
            if self.table[0][i] == y:
                idx_y = i
                break

        return self.table[idx_x][idx_y]

    def put(self, x, y, data):
        idx_x, idx_y = None, None

        for i in range(1, len(self.terminals) + len(self.nonterminals) + 1):
            if self.table[i][0] == x:
                idx_x = i
                break

        for i in range(1, len(self.terminals) + 1):
            if self.table[0][i] == y:
                idx_y = i
                break

        # if self.table[idx_x][idx_y] is not None:
        #     raise Exception('Invalid grammar!')

        self.table[idx_x][idx_y] = data

    def ll1_table(self):
        self._init_ll1_table()

        i = 1

        for name, production in self.productions.items():
            for idx, elem in enumerate(production):
                if elem == Grammar.EPSILON:
                    _follow = self.follow_table[name]

                    for f in _follow:
                        y = f if f != Grammar.EPMTY else Grammar.EPSILON
                        self.put(name, y, (name, idx, i))

                else:
                    if elem[0] in self.terminals:
                        _first = (elem[0])
                    else:
                        _first = self.first_table[elem[0]]

                    for f in _first:
                        self.put(name, f, (name, idx, i))
                i += 1

    def save_table(self):
        with open('./ParserOutput.txt', 'w') as f:
            pprint(self.table, f)

if __name__ == '__main__':
    g = Grammar(file=FILE)
    g.read()

    # print(f'Nonterminals: {g.nonterminals}')
    # print(f'Terminals: {g.terminals}')
    # print(f'Start: {g.start}')
    print(f'Productions: {g.productions}')
    # print(f'Productions for nonterminal Statement: {g.productions_for_nonterminal("A")}')
    # print(f'CFG check: {g.check()}')

    g.first_follow()
    print(f'First: {g.first_table}')
    print(f'Follow: {g.follow_table}')

    g.ll1_table()
    g.save_table()
    print('Table:')
    pprint(g.table)