from Lab_5 import Grammar
import unittest


class TestGrammar(unittest.TestCase):
    def setUp(self):
        self.g = Grammar()
        self.P1, self.P2, self.P3, self.P4, self.P5 = self.g.ReturnProductions()

    def test_elim_epsilon(self):
        expected_result = {'S': ['dB', 'd', 'dS', 'aBdB'],
                           'A': ['d', 'dS', 'aBdB'],
                           'B': ['a', 'aS', 'AC', 'd', 'dS', 'aBdB'],
                           'D': ['AB'],
                           'C': ['bC', 'b']
                           }
        self.assertEqual(self.P1, expected_result)

    def test_elim_unit_prod(self):
        expected_result = {'S': ['dB', 'd', 'dS', 'aBdB'],
                           'A': ['d', 'dS', 'aBdB'],
                           'B': ['a', 'aS', 'AC', 'd', 'dS', 'aBdB'],
                           'D': ['AB'],
                           'C': ['bC', 'b']
                           }
        self.assertEqual(self.P2, expected_result)

    def test_elim_inaccesible_sumb(self):
        expected_result = {'S': ['dB', 'd', 'dS', 'aBdB'],
                           'A': ['d', 'dS', 'aBdB'],
                           'B': ['a', 'aS', 'AC', 'd', 'dS', 'aBdB'],
                           'C': ['bC', 'b']
                           }
        self.assertEqual(self.P3, expected_result)

    def test_elim_unprod_symb(self):
        expected_result = {'S': ['dB', 'd', 'dS', 'aBdB'],
                           'A': ['d', 'dS', 'aBdB'],
                           'B': ['a', 'aS', 'AC', 'd', 'dS', 'aBdB'],
                           'C': ['bC', 'b']
                           }
        self.assertEqual(self.P4, expected_result)

    def test_transform_to_cnf(self):
        expected_result = {'S': ['DE', 'd', 'DF', 'GH'],
                           'A': ['d', 'DF', 'GH'],
                           'B': ['a', 'IF', 'AC', 'd', 'DF', 'GH'],
                           'C': ['JK', 'b'],
                           'D': ['d'],
                           'E': ['B'],
                           'F': ['S'],
                           'G': ['aB'],
                           'H': ['dB'],
                           'I': ['a'],
                           'J': ['b'],
                           'K': ['C']
                           }
        self.assertEqual(self.P5, expected_result)


if __name__ == '__main__':
    unittest.main()
