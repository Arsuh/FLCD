FILE = './Grammars/g4.txt'

class Grammar:
    EPSILON = 'EPSILON'
    EPMTY = '$'

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

if __name__ == '__main__':
    g = Grammar(file=FILE)
    g.read()

    # print(f'Nonterminals: {g.nonterminals}')
    # print(f'Terminals: {g.terminals}')
    # print(f'Start: {g.start}')
    # print(f'Productions: {g.productions}')
    # print(f'Productions for nonterminal Statement: {g.productions_for_nonterminal("A")}')
    # print(f'CFG check: {g.check()}')

    g.first_follow()
    print(f'First: {g.first_table}')
    print(f'Follow: {g.follow_table}')