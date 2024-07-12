class RegularGrammar:
    def __init__(self, start_symbol, terminals, non_terminals, productions):
        self.start_symbol = start_symbol
        self.productions = productions
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.reversed_productions = self._reverse_productions()

    def from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            start_symbol = lines[0].strip()
            terminals = lines[1].strip().split()
            non_terminals = lines[2].strip().split()
            lines = lines[3:]
            productions = {}
            for line in lines:
                line = line.strip()
                if '->' in line:
                    left, right = line.split('->')
                    left = left.strip()
                    right = right.strip()
                    if left not in productions:
                        productions[left] = []
                    productions[left].append(right)
            return RegularGrammar(start_symbol, terminals, non_terminals, productions)

    def _reverse_productions(self):
        reversed_productions = {}
        for left, rights in self.productions.items():
            for right in rights:
                if right not in reversed_productions:
                    reversed_productions[right] = []
                reversed_productions[right].append(left)
        return reversed_productions

    def check_string(self, input_string):
        stack = list(input_string)
        derivation_steps = []

        while len(stack) > 1 or (stack and stack[0] != self.start_symbol):
            matched = False
            aux = stack.copy()
            for length in range(1, len(stack) + 1):
                for right, lefts in self.reversed_productions.items():
                    if ''.join(stack[-length:]) == right:
                        derivation_steps.append((lefts[0], ''.join(stack)))
                        stack = stack[:-length] + [lefts[0]]
                        matched = True
                        break

                # Check for epsilon productions
                aux.append('epsilon')
                for right, lefts in self.reversed_productions.items():
                    if ''.join(aux[-1:]) == right:
                        derivation_steps.append((lefts[0], ''.join(stack)))
                        aux = aux[:-1] + [lefts[0]]
                        matched = True
                        print("Epsilon production")
                        stack = aux
                        break
                

                if matched:
                    break
            if not matched:
                print("No valid derivation found.")
                return False

        derivation_steps.append((self.start_symbol, ''.join(stack)))

        print("Derivation steps:")
        derivation_steps.reverse()
        for step in derivation_steps:
            print(f"{step[0]} -> {step[1]}")

        return stack == [self.start_symbol]

def main():
    grammar_file = 'grammar.txt'
    input_string = input('Enter a string to check: ').strip()

    grammar = RegularGrammar.from_file(grammar_file)
    if grammar.check_string(input_string):
        print(f'The string "{input_string}" is accepted by the grammar.')
    else:
        print(f'The string "{input_string}" is not accepted by the grammar.')

if __name__ == '__main__':
    main()
