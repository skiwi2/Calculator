from decimal import Decimal
from calculator.calculator import Calculator
from calculator.tokens import ValueToken
from calculator.tokens import OperatorToken

__author__ = 'Frank van Heeswijk'

import unittest


class CalculatorTest(unittest.TestCase):
    def test_evaluate(self):
        calculator = Calculator()
        self.assertEqual(Decimal(4), calculator.evaluate("4"))

    def test_tokenize_value(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(2))
        ]
        self.assertListEqual(expected, calculator.tokenize("2"))

    def test_tokenize_value_parentheses(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(2))
        ]
        self.assertListEqual(expected, calculator.tokenize("( 2 )"))

    def test_tokenize_value_parentheses_missing_right(self):
        calculator = Calculator()
        self.assertRaises(RuntimeError, calculator.tokenize, "2 )")

    def test_tokenize_value_parentheses_missing_left(self):
        calculator = Calculator()
        self.assertRaises(RuntimeError, calculator.tokenize, "( 2")

    def test_tokenize_decimal(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal("6.2"))
        ]
        self.assertListEqual(expected, calculator.tokenize("6.2"))

    def test_tokenize_operator(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(2)),
            ValueToken(Decimal(4)),
            OperatorToken('+')
        ]
        self.assertListEqual(expected, calculator.tokenize("2 + 4"))

    def test_tokenize_operator_parentheses(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(2)),
            ValueToken(Decimal(4)),
            OperatorToken('+'),
        ]
        self.assertListEqual(expected, calculator.tokenize("( 2 + 4 )"))

    def test_tokenize_multiple_parentheses(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(3)),
            ValueToken(Decimal(2)),
            ValueToken(Decimal(4)),
            OperatorToken('+'),
            OperatorToken('*')
        ]
        self.assertListEqual(expected, calculator.tokenize("( 3 * ( ( 2 ) + ( 4 ) ) )"))

    def test_tokenize_multiple_parentheses_decimal(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal("3.5")),
            ValueToken(Decimal("2.7")),
            ValueToken(Decimal("4.8")),
            OperatorToken('+'),
            OperatorToken('*')
        ]
        self.assertListEqual(expected, calculator.tokenize("( 3.5 * ( ( 2.7 ) + ( 4.8 ) ) )"))

    def test_tokenize_operator_precedence(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(5)),
            ValueToken(Decimal(3)),
            ValueToken(Decimal(4)),
            OperatorToken('*'),
            OperatorToken('+')
        ]
        self.assertListEqual(expected, calculator.tokenize("5 + 3 * 4"))

    def test_tokenize_operator_precedence_with_parentheses(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(5)),
            ValueToken(Decimal(3)),
            OperatorToken('+'),
            ValueToken(Decimal(4)),
            OperatorToken('*')
        ]
        self.assertListEqual(expected, calculator.tokenize("( 5 + 3 ) * 4"))

if __name__ == '__main__':
    unittest.main()
