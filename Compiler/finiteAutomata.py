STATES_INDEX = 0
ALPHABET_INDEX = 1
INITIAL_STATE_INDEX = 2
FINAL_STATES_INDEX = 3

class FA:
    def __init__(self, fa_path) -> None:        
        self.states = []
        self.alphabet = []
        self.initial_state = None
        self.final_states = []
        self.transitions = []

        self._load_data(fa_path)

    def _load_data(self, fa_path):
        with open(fa_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')

        for state in lines[STATES_INDEX].split(' = ')[-1].split(' '):
            self.states.append(state)

        for character in lines[ALPHABET_INDEX].split(' = ')[-1].split(' '):
            self.alphabet.append(character)

        self.initial_state = lines[INITIAL_STATE_INDEX].split(' = ')[-1]

        for state in lines[FINAL_STATES_INDEX].split(' = ')[-1].split(' '):
            self.final_states.append(state)

        for transition in lines[FINAL_STATES_INDEX+1:]:
            initial, final, value = transition.split(' ')
            self.transitions.append((initial, final, value))

    def _transition(self, current_state, current_character):
        for transition in self.transitions:
            if current_state == transition[0] and current_character == transition[2]:
                return transition

        return None
    
    def check(self, value: str):
        current_state = self.initial_state

        for character in value:
            if character not in self.alphabet:
                return False

            transition = self._transition(current_state, character)

            if transition is None:
                return False

            current_state = transition[1]


        return True


def menu(fa: FA):
    print('1. States')
    print('2. Alphabet')
    print('3. Initial State')
    print('4. Final states')
    print('5. Transitions')
    print('0. Exit')

    choice = int(input('Enter choice: '))

    while choice != 0:
        match choice:
            case 1:
                print(fa.states)
            case 2:
                print(fa.alphabet)
            case 3:
                print(fa.initial_state)
            case 4:
                print(fa.final_states)
            case 5:
                print(fa.transitions)
            case _:
                return

        print('1. States')
        print('2. Alphabet')
        print('3. Initial State')
        print('4. Final states')
        print('5. Transitions')
        print('0. Exit')

        choice = int(input('Enter choice: '))
        

if __name__ == '__main__':
    fa_identifier = FA(fa_path='./FiniteAutomata/FA_identifier.in')
    fa_integer = FA(fa_path='./FiniteAutomata/FA_integer_constant.in')

    # menu(fa_identifier)

    print(fa_identifier.check('a'))
    print(fa_identifier.check('abcd'))
    print(fa_identifier.check('abcd'))
    print(fa_identifier.check('Abcd'))
    print(fa_identifier.check('_01abcd'))
    print(fa_identifier.check('7a7abcd'))
    print(fa_identifier.check('A777abcd_'))

    print()

    print(fa_integer.check('10'))
    print(fa_integer.check('0'))
    print(fa_integer.check('-15'))
    print(fa_integer.check('0010'))
    print(fa_integer.check('-0'))
    print(fa_integer.check('1A0'))
    print(fa_integer.check('-3540000000'))