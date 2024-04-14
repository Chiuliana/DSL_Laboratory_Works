import random

class Grammar:
    def __init__(self):
        self.V_n = {'S', 'F', 'L'}
        self.V_t = {'a', 'b', 'c', 'd'}
        self.P = {
            'S': ['bS', 'aF', 'd'],
            'F': ['cF', 'dF', 'aL', 'b'],
            'L': ['aL', 'c']
        }

    def generate_string(self, start_symbol='S', max_length=10):
        if max_length == 0:
            return ''
        if start_symbol not in self.V_n:
            return start_symbol
        production_choices = self.P[start_symbol]
        chosen_production = random.choice(production_choices)
        generated_string = ''
        for symbol in chosen_production:
            generated_string += self.generate_string(symbol, max_length - 1)
        return generated_string

    def to_finite_automaton(self):
        states = self.V_n.union(self.V_t)
        alphabet = self.V_t
        transitions = {}
        for non_terminal, productions in self.P.items():
            for production in productions:
                if len(production) == 2:
                    if (non_terminal, production[0]) in transitions:
                        transitions[(non_terminal, production[0])].append(production[1])
                    else:
                        transitions[(non_terminal, production[0])] = [production[1]]
                elif len(production) == 1:
                    if (non_terminal, production) in transitions:
                        transitions[(non_terminal, production)].append(non_terminal)
                    else:
                        transitions[(non_terminal, production)] = [non_terminal]
        initial_state = 'S'
        accepting_states = {'S', 'F', 'L'}  # Assuming all non-terminals are accepting states
        return FiniteAutomaton(states, alphabet, transitions, initial_state, accepting_states)

    def transform_grammar(self):
        productions = []

        for non_terminal, production_list in self.P.items():
            for production in production_list:
                productions.append(f"{non_terminal} -> {production}")
        return productions

    def classify_grammar(self, terminals, non_terminals):
        # Check if the grammar is regular
        productions = self.transform_grammar()
        is_regular = True
        for production in productions:
            left, right = production.split(" -> ")
            left = left.strip()
            right = right.strip()
            if len(right) > 2:
                is_regular = False
                break
            if len(right) == 2 and right[0] not in non_terminals:
                is_regular = False
                break

        # Check if the grammar is context-free
        is_context_free = True
        for production in productions:
            left, right = production.split(" -> ")
            left = left.strip()
            right = right.strip()
            if len(left) != 1:
                is_context_free = False
                break

        # Check if the grammar is context-sensitive
        is_context_sensitive = True
        for production in productions:
            left, right = production.split(" -> ")
            left = left.strip()
            right = right.strip()
            if len(left) > len(right):
                is_context_sensitive = False
                break

        # Determine the type of grammar
        if is_regular:
            return "Regular Grammar"
        elif is_context_free:
            return "Context-Free Grammar"
        elif is_context_sensitive:
            return "Context-Sensitive Grammar"
        else:
            return "Unrestricted Grammar"

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accepting_states = accepting_states

    def string_belongs_to_language(self, input_string):
        current_states = {self.initial_state}
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if (state, symbol) in self.transitions:
                    next_states.update(self.transitions[(state, symbol)])
            current_states = next_states
        return any(state in self.accepting_states for state in current_states)

# Test Grammar functionality
grammar = Grammar()

# Generate 5 valid strings from the grammar
print("Generated strings:")
for _ in range(5):
    generated_string = grammar.generate_string()
    print(generated_string)

# Convert Grammar to Finite Automaton
finite_automaton = grammar.to_finite_automaton()

# Test strings with the Finite Automaton
test_strings = ['abcc', 'bdab', 'cddd', 'abcb', 'bbaac']
for string in test_strings:
    if finite_automaton.string_belongs_to_language(string):
        print(f"'{string}' belongs to the language.")
    else:
        print(f"'{string}' does not belong to the language.")

# Classify the grammar based on Chomsky hierarchy
gram_classification = grammar.classify_grammar(grammar.V_t, grammar.V_n)
print("Grammar Classification:", gram_classification)