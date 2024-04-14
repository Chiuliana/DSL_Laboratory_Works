class Grammar:
    def __init__(self, non_terminals=None, terminals=None, rules=None):
        if non_terminals is None:
            non_terminals = []
        if terminals is None:
            terminals = []
        if rules is None:
            rules = {}
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules

    def remove_epsilon(self):
        nt_epsilon = []
        for key, value in self.rules.items():
            s = key
            productions = value
            for p in productions:
                if p == 'epsilon':
                    nt_epsilon.append(s)

        updated_grammar = self.rules.copy()
        for key, value in self.rules.items():
            for ep in nt_epsilon:
                for v in value:
                    prod_copy = v
                    if ep in prod_copy:
                        for c in prod_copy:
                            if c == ep:
                                updated_grammar[key].append(prod_copy.replace(c, ''))
        for key, value in self.rules.items():
            if key in nt_epsilon and len(value) < 2:
                del updated_grammar[key]
            else:
                for v in value:
                    if v == 'epsilon':
                        updated_grammar[key].remove(v)
        self.rules = updated_grammar.copy()
        return updated_grammar

    def eliminate_unit_prod(self):
        updated_grammar = self.rules.copy()
        for key, value in self.rules.items():
            for v in value:
                if len(v) == 1 and v in self.non_terminals:
                    updated_grammar[key].remove(v)
                    for p in self.rules[v]:
                        updated_grammar[key].append(p)
        self.rules = updated_grammar.copy()
        return updated_grammar

    def eliminate_inaccessible(self):
        reachable = set()
        reachable.add(self.non_terminals[0])  # Start symbol
        updated_grammar = {}
        while True:
            old_len = len(reachable)
            for variable, productions in self.rules.items():
                if variable in reachable:
                    for production in productions:
                        for symbol in production:
                            if symbol in self.non_terminals:
                                reachable.add(symbol)
            if len(reachable) == old_len:
                break
        for variable, productions in self.rules.items():
            if variable in reachable:
                updated_grammar[variable] = productions
        self.rules = updated_grammar.copy()
        return updated_grammar

    def remove_unprod(self):
        productive = set()
        updated_grammar = self.rules.copy()
        terminals = {symbol for productions in self.rules.values() for production in productions for symbol in
                     production if symbol not in self.non_terminals}

        while True:
            old_len = len(productive)
            for variable, productions in updated_grammar.items():
                for production in productions:
                    if all(symbol in productive or symbol in terminals for symbol in production):
                        productive.add(variable)
            if len(productive) == old_len:
                break

        for variable, productions in self.rules.items():
            if variable in productive:
                updated_productions = []
                for production in productions:
                    if all(symbol in productive or symbol in terminals for symbol in production):
                        updated_productions.append(production)
                updated_grammar[variable] = updated_productions
            else:
                updated_grammar.pop(variable, None)

        self.rules = updated_grammar.copy()
        return updated_grammar

    def transform_to_cnf(self):
        rhs_to_non_terminal = {}
        old_non_terminals = list(self.rules)

        new_rules = {}
        for non_terminal in list(self.rules):
            new_rules[non_terminal] = set()
            for production in self.rules[non_terminal]:
                while len(production) > 2:
                    first_two_symbols = production[:2]

                    if first_two_symbols in rhs_to_non_terminal:
                        new_non_terminal = rhs_to_non_terminal[first_two_symbols]
                    else:
                        new_non_terminal = self.create_new_non_terminal()
                        new_rules[new_non_terminal] = {first_two_symbols}
                        rhs_to_non_terminal[first_two_symbols] = new_non_terminal

                    production = new_non_terminal + production[2:]

                new_rules[non_terminal].add(production)

        for non_terminal, productions in list(new_rules.items()):
            temp_productions = productions.copy()
            for production in temp_productions:
                if len(production) == 2 and any(symbol in self.terminals for symbol in production):
                    new_production = []
                    for symbol in production:
                        if symbol in self.terminals:
                            if symbol in rhs_to_non_terminal:
                                new_non_terminal = rhs_to_non_terminal[symbol]
                            else:
                                new_non_terminal = self.create_new_non_terminal()
                                new_rules[new_non_terminal] = {symbol}
                                rhs_to_non_terminal[symbol] = new_non_terminal
                            new_production.append(new_non_terminal)
                        else:
                            new_production.append(symbol)
                    productions.remove(production)
                    productions.add(''.join(new_production))

        self.rules = {nt: new_rules[nt] for nt in old_non_terminals +
                      list(set(new_rules) - set(old_non_terminals))}
        return self.rules

    def create_new_non_terminal(self):
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for letter in alphabet:
            if letter not in self.non_terminals:
                self.non_terminals.append(letter)
                return letter
        for letter in alphabet:
            for num in range(100):
                new_symbol = f'{letter}{num}'
                if new_symbol not in self.non_terminals:
                    self.non_terminals.append(new_symbol)
                    return new_symbol
        raise ValueError("Exhausted all possible non-terminal symbols.")

    def print_grammar(self):
        for variable, productions in self.rules.items():
            print(f"{variable} -> {' | '.join(productions)}")


