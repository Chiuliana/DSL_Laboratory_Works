class FiniteAutomatom:
    def __init__(self):
        self.Q = ['q0','q1','q2','q3']
        self.Sigma = ['a','b']
        self.Delta = {
            ('q0', 'a') : ['q1'],
            ('q0', 'b') : ['q0'],
            ('q1', 'a') : ['q2', 'q3'],  # Modified transition
            ('q1', 'b') : ['q1'],
            ('q2', 'a') : ['q3'],
            ('q2', 'b') : ['q0'],
            ('q3', 'a') : ['q3'],
            ('q3', 'b') : ['q0']
        }
        self.q0 = 'q0'
        self.F = ['q3']

class Grammar:
    def __init__(self, S, V_n, V_t, P):
        self.S = S
        self.V_n = V_n
        self.V_t  = V_t
        self.P = P

    def show_gramamr(self):
        print("VN = {", ', '.join(map(str, self.V_n)), '}' )
        print("VT = {", ', '.join(map(str, self.V_t)), '}' )
        print("P = { ")
        for el in self.P:
            a,b,c = el
            print(f"    {a} -> {b}{c}")
        print("}")
