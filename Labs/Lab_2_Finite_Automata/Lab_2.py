from automathon import DFA, NFA

class FiniteAutomaton:
    def __init__(self):
        self.Q = ['q0', 'q1', 'q2', 'q3']
        self.Sigma = ['a', 'b']
        self.Delta = {
            ('q0', 'a'): ['q1'],
            ('q0', 'b'): ['q0'],
            ('q1', 'a'): ['q2', 'q3'],
            ('q2', 'a'): ['q3'],
            ('q2', 'b'): ['q0'],
        }
        self.q0 = 'q0'
        self.F = ['q3']

    def convert_to_grammar(self):
        S = self.Q[0]
        V_n = self.Q
        V_t = self.Sigma
        P = [(state, symbol, next_state) for state in self.Q for symbol in self.Sigma
             for next_state in self.Delta.get((state, symbol), [])]
        for final_state in self.F:
            P.append((final_state, '', 'e'))
        return Grammar(S, V_n, V_t, P)

    def check_deterministic(self):
        return all(len(value) <= 1 for value in self.Delta.values())

    def nfa_to_dfa(self):
        input_symbols = self.Sigma
        initial_state = self.q0
        states = []
        final_states = set()  # Using a set to collect unique final states

        transitions = {}
        new_states = ['q0']
        while new_states:
            for state in new_states:
                new_states.remove(state)
                if state not in transitions.keys():
                    transitions[state] = {}
                    temp_state = state.split(',')
                    for el in input_symbols:
                        transitions[state].update({el: ''})
                        for s in temp_state:
                            if (s, el) in self.Delta.keys():
                                transitions[state][el] += ','.join(self.Delta[(s, el)]) + ','
                                if len(','.join(transitions[state][el])) >= len(','.join(state)):
                                    new_states.append(transitions[state][el].rstrip(','))
                        transitions[state][el] = transitions[state][el].rstrip(',')
                    # Remove empty strings from the secondary dictionaries
                    transitions[state] = {key: value for key, value in transitions[state].items() if value != ''}

        for key, _ in transitions.items():
            states.append(key)

        # Function to perform epsilon closure
        def epsilon_closure(state):
            closure = {state}
            stack = [state]
            while stack:
                current_state = stack.pop()
                if current_state in self.Delta and ('', '') in self.Delta[current_state]:
                    for next_state in self.Delta[current_state][('', '')]:
                        if next_state not in closure:
                            closure.add(next_state)
                            stack.append(next_state)
            return closure

        # Identify final states reachable from initial final states via epsilon transitions
        for el in self.F:
            for state in epsilon_closure(el):
                final_states.add(state)

        # Check if any state contains 'q3'
        for state in states:
            if 'q3' in state:
                final_states.add(state)

        print(f"Q = {states}")
        print(f"Sigma = {input_symbols}")
        print(f"Delta = {transitions}")
        print(f"q0 = {initial_state}")
        print(f"F = {list(final_states)}")  # Convert set to list

        dfa = DFA(
            states,
            input_symbols,
            transitions,
            initial_state,
            list(final_states)  # Convert set to list
        )
        dfa.view("DFA")


class Grammar:
    def __init__(self, S, V_n, V_t, P):
        self.S = S
        self.V_n = V_n
        self.V_t = V_t
        self.P = P

    def show_grammar(self):
        print("V_N = {", ', '.join(map(str, self.V_n)), '}')
        print("V_T = {", ', '.join(map(str, self.V_t)), '}')
        print("P = { ")
        for el in self.P:
            a, b, c = el
            print(f"    {a} -> {b}{c}")
        print("}")


# main
finite_automaton = FiniteAutomaton()
grammar = finite_automaton.convert_to_grammar()
print("Grammar:")
grammar.show_grammar()

print()

if not finite_automaton.check_deterministic():
    print("It's a Non-Deterministic Finite Automaton\n")
else:
    print("It's a Deterministic Finite Automaton\n")

print("Deterministic Finite Automaton:")
finite_automaton.nfa_to_dfa()

# NFA to compare graphically with DFA
NFA({'q0', 'q1', 'q2', 'q3'}, {'a', 'b'},
    {'q0': {'a': {'q1'}, 'b': {'q0'}},
     'q1': {'a': {'q2', 'q3'}},
     'q2': {'b': {'q0'}, 'a': {'q3'}}},
    'q0', {'q3'}).view("NFA")
