class Grammar:
    def __init__(self):
        self.P = {
            'S': ['dB', 'A'],
            'A': ['d', 'dS', 'aBdB'],
            'B': ['a', 'aS', 'AC'],
            'D': ['AB'],
            'C': ['bC', 'epsilon']
        }
        self.V_N = ['S', 'A', 'B', 'C', 'D']
        self.V_T = ['a', 'b', 'd']

    def elim_epsilon(self):
        nt_epsilon = []
        for key, value in self.P.items():
            s = key
            productions = value
            for p in productions:
                if p == 'epsilon':
                    nt_epsilon.append(s)

        for key, value in self.P.items():
            for ep in nt_epsilon:
                for v in value:
                    prod_copy = v
                    if ep in prod_copy:
                        for c in prod_copy:
                            if c == ep:
                                value.append(prod_copy.replace(c, ''))

        P1 = self.P.copy()
        for key, value in self.P.items():
            if key in nt_epsilon and len(value) < 2:
                del P1[key]
            else:
                for v in value:
                    if v == 'epsilon':
                        P1[key].remove(v)

        print(f"1. Eliminating epsilon productions:")
        for key, value in P1.items():
            print(f"{key} -> {' | '.join(value)}")
        print("------------------------------------------------")
        self.P = P1.copy()
        return P1

    def elim_unit_prod(self):
        P2 = self.P.copy()
        for key, value in self.P.items():
            for v in value:
                if len(v) == 1 and v in self.V_N:
                    P2[key].remove(v)
                    for p in self.P[v]:
                        P2[key].append(p)
        print(f"2. Eliminating unit productions:")
        for key, value in P2.items():
            print(f"{key} -> {' | '.join(value)}")
        print("------------------------------------------------")
        self.P = P2.copy()
        return P2

    def elim_inaccesible_symb(self):
        P3 = self.P.copy()
        accesible_symbols = self.V_N
        for key, value in self.P.items():
            for v in value:
                for s in v:
                    if s in accesible_symbols:
                        accesible_symbols.remove(s)

        for el in accesible_symbols:
            del P3[el]

        print(f"3. Eliminating inaccessible symbols:")
        for key, value in P3.items():
            print(f"{key} -> {' | '.join(value)}")
        print("------------------------------------------------")
        self.P = P3.copy()
        return P3

    def elin_unnprod_symb(self):
        P4 = self.P.copy()
        for key, value in self.P.items():
            count = 0
            for v in value:
                if len(v) == 1 and v in self.V_T:
                    count += 1
            if count == 0:
                del P4[key]
                for k, v in self.P.items():
                    for e in v:
                        if k == key:
                            break
                        else:
                            if key in e:
                                P4[key].remove(e)

        for key, value in self.P.items():
            for v in value:
                for c in v:
                    if c.isupper() and c not in P4.keys():
                        P4[key].remove(v)
                        break

        print(f"4. Eliminating unproductive symbols:")
        for key, value in P4.items():
            print(f"{key} -> {' | '.join(value)}")
        print("------------------------------------------------")
        self.P = P4.copy()
        return P4

    def transf_to_cnf(self):
        P5 = self.P.copy()
        temp = {}
        vocabulary = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                      'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        free_symbols = [v for v in vocabulary if v not in self.P.keys()]
        for key, value in self.P.items():
            for v in value:
                if (len(v) == 1 and v in self.V_T) or (len(v) == 2 and v.isupper()):
                    continue
                else:
                    left = v[:len(v) // 2]
                    right = v[len(v) // 2:]
                    if left in temp.values():
                        temp_key1 = ''.join([i for i in temp.keys() if temp[i] == left])
                    else:
                        temp_key1 = free_symbols.pop(0)
                        temp[temp_key1] = left
                    if right in temp.values():
                        temp_key2 = ''.join([i for i in temp.keys() if temp[i] == right])
                    else:
                        temp_key2 = free_symbols.pop(0)
                        temp[temp_key2] = right

                    P5[key] = [temp_key1 + temp_key2 if item == v else item for item in P5[key]]

        for key, value in temp.items():
            P5[key] = [value]

        print(f"5. Obtain Chomsky Normal Form(CNF):")
        for key, value in P5.items():
            print(f"{key} -> {' | '.join(value)}")
        print("------------------------------------------------")
        return P5

    def ReturnProductions(self):
        print(f"Initial Grammar:")
        for key, value in self.P.items():
            print(f"{key} -> {' | '.join(value)}")
        print("------------------------------------------------")
        P1 = self.elim_epsilon()
        P2 = self.elim_unit_prod()
        P3 = self.elim_inaccesible_symb()
        P4 = self.elin_unnprod_symb()
        P5 = self.transf_to_cnf()
        return P1, P2, P3, P4, P5

if __name__ == "__main__":
    g = Grammar()
    P1, P2, P3, P4, P5 = g.ReturnProductions()