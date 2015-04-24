from decimal import Decimal
from calculator.calculator import Calculator

__author__ = 'Frank van Heeswijk'

import unittest

class CalculatorTest(unittest.TestCase):
    def test_evaluate(self):
        calculator = Calculator()
        self.assertEqual(Decimal(4), calculator.evaluate("4"))

if __name__ == '__main__':
    unittest.main()
