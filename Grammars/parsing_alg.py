from grammar import Grammar
from pprint import pprint

GRAMMAR = './Grammars/g4.txt'
PIF = './PIF.out'
PIF = './seq.txt'

class Parse:
    def __init__(self):
        self.g = Grammar(file=GRAMMAR)

        self.seq = []
        self._read_seq(file=PIF)

    def _read_seq(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            data = f.read()

        data = data.split('), ')
        for d in data:
            a = d.split(', ')[0][2:-1]
            self.seq.append(a)

    def parse(self):
        self.g.read()
        self.g.first_follow()
        self.g.ll1_table()
        self.g.save_table()


        return self._parse()

    def _parse(self):
        beta = []
        beta.append(Grammar.EPSILON)
        beta.append(self.g.start)

        alpha = []
        alpha.append(Grammar.EPSILON)
        for c in self.seq:
            alpha.append(c)
        out = []

        t_i = 2
        # table = {self.g.start: (1, self.g.start, 0, 0)}
        table = [(1, self.g.start, 0, 0)]

        s = None

        go = True
        while go:
            h_b = beta[-1]
            h_a = alpha[-1]

            m = self.g.get_move(h_b, h_a)

            if m is not None and m != Grammar.POP and m != Grammar.ACC:
                beta.pop()

                production = self.g.productions[m[0]][m[1]]

                rs = 0
                for c in production.split(' ')[::-1]:
                    if c != Grammar.EPSILON:
                        beta.append(c)

                        pr = None
                        for x in table[::-1]:
                            if x[1] == h_b:
                                pr = x[0]

                        table.append((t_i, c, pr, rs))
                        rs = t_i

                        t_i += 1

                out.append(m[2])

            elif m == Grammar.POP:
                alpha.pop()
                beta.pop()
            elif m == Grammar.ACC:
                go = False
                s = 'ACC'
            else:
                go = False
                s = 'ERR'

        print(s)
        pprint(table)

        return out
                

if __name__ == '__main__':
    p = Parse()
    print(p.seq)
    parsing_tree = p.parse()
    print(parsing_tree)