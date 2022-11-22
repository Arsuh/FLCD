FILE = './Grammars/g2.txt'

class Grammar:
    def __init__(self, file):
        self.file = file

        self.nonterminals = []
        self.terminals = []
        self.start = None
        self.productions = {}

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

if __name__ == '__main__':
    g = Grammar(file=FILE)
    g.read()

    print(f'Nonterminals: {g.nonterminals}')
    print(f'Terminals: {g.terminals}')
    print(f'Start: {g.start}')
    print(f'Productions: {g.productions}')
    print(f'Productions for nonterminal Statement: {g.productions_for_nonterminal("Statement")}')
    print(f'CFG check: {g.check()}')
    