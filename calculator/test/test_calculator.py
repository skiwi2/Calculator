from decimal import Decimal
from calculator.calculator import Calculator
from calculator.tokens import ValueToken, LeftParenthesesToken, RightParenthesesToken
from calculator.tokens import OperatorToken

__author__ = 'Frank van Heeswijk'

import unittest


class CalculatorTest(unittest.TestCase):
    def test_evaluate(self):
        calculator = Calculator()
        self.assertEqual(Decimal(4), calculator.evaluate("4"))
        self.assertEqual(Decimal(21), calculator.evaluate("7 * 3"))
        self.assertEqual(Decimal(11), calculator.evaluate("2 * 4 + 3"))
        self.assertEqual(Decimal(45), calculator.evaluate("( 3 * ( 2 + 5 ) ) + 6 * ( 4 )"))
        self.assertEqual(Decimal("25.92"), calculator.evaluate("2.7 * ( 3.2 + 6.4 )"))
        self.assertEqual(Decimal(1), calculator.evaluate("- 2 * - 4 + - 7"))

    def test_evaluate_operators(self):
        calculator = Calculator()
        self.assertEqual(Decimal(3), calculator.evaluate("+ 3"))
        self.assertEqual(Decimal(-3), calculator.evaluate("- 3"))
        self.assertEqual(Decimal(6), calculator.evaluate("2 * 3"))
        self.assertEqual(Decimal(2), calculator.evaluate("6 / 3"))
        self.assertEqual(Decimal(5), calculator.evaluate("2 + 3"))
        self.assertEqual(Decimal(3), calculator.evaluate("7 - 4"))

    def test_evaluate_operator_precedences(self):
        calculator = Calculator()
        self.assertEqual(Decimal(-14), calculator.evaluate("- 3 * 5 + + 1"))
        self.assertEqual(Decimal("6.5"), calculator.evaluate("8 / - 16 - - 7"))
        self.assertEqual(Decimal(30), calculator.evaluate("5 * 3 * 8 / 4 / 2 * 6 / 3"))
        self.assertEqual(Decimal(-3), calculator.evaluate("2 + 3 + 4 - 5 - 8 + 6 + 4 - 9"))

    def test_tokenize_value(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(3))
        ]
        self.assertListEqual(expected, calculator.tokenize("3"))

    def test_tokenize_value_parentheses(self):
        calculator = Calculator()
        expected = [
            LeftParenthesesToken(),
            ValueToken(Decimal(3)),
            RightParenthesesToken()
        ]
        self.assertListEqual(expected, calculator.tokenize("( 3 )"))

    def test_tokenize_expression(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(2)),
            OperatorToken('*'),
            LeftParenthesesToken(),
            ValueToken(Decimal(3)),
            OperatorToken('+'),
            ValueToken(Decimal(4)),
            RightParenthesesToken()
        ]
        self.assertListEqual(expected, calculator.tokenize("2 * ( 3 + 4 )"))

    def test_tokenize_expression_no_parentheses(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(2)),
            OperatorToken('*'),
            ValueToken(Decimal(3)),
            OperatorToken('+'),
            ValueToken(Decimal(4)),
        ]
        self.assertListEqual(expected, calculator.tokenize("2 * 3 + 4"))

    def test_tokenize_unary_minus_start_of_expression(self):
        calculator = Calculator()
        expected = [
            OperatorToken('u-'),
            ValueToken(Decimal(3))
        ]
        self.assertListEqual(expected, calculator.tokenize("- 3"))

    def test_tokenize_unary_minus_start_of_expression_inside_parentheses(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(2)),
            OperatorToken('*'),
            LeftParenthesesToken(),
            OperatorToken('u-'),
            ValueToken(Decimal(3)),
            RightParenthesesToken()
        ]
        self.assertListEqual(expected, calculator.tokenize("2 * ( - 3 )"))

    def test_tokenize_unary_minus_after_operator(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(3)),
            OperatorToken('*'),
            OperatorToken('u-'),
            ValueToken(Decimal(2))
        ]
        self.assertListEqual(expected, calculator.tokenize("3 * - 2"))

    def test_tokenize_unary_plus_start_of_expression(self):
        calculator = Calculator()
        expected = [
            OperatorToken('u+'),
            ValueToken(Decimal(3))
        ]
        self.assertListEqual(expected, calculator.tokenize("+ 3"))

    def test_tokenize_unary_plus_start_of_expression_inside_parentheses(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(2)),
            OperatorToken('*'),
            LeftParenthesesToken(),
            OperatorToken('u+'),
            ValueToken(Decimal(3)),
            RightParenthesesToken()
        ]
        self.assertListEqual(expected, calculator.tokenize("2 * ( + 3 )"))

    def test_tokenize_unary_plus_after_operator(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(3)),
            OperatorToken('*'),
            OperatorToken('u+'),
            ValueToken(Decimal(2))
        ]
        self.assertListEqual(expected, calculator.tokenize("3 * + 2"))

    def test_rpn_value(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(2))
        ]
        self.assertListEqual(expected, calculator.to_rpn(calculator.tokenize("2")))

    def test_rpn_value_parentheses(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(2))
        ]
        self.assertListEqual(expected, calculator.to_rpn(calculator.tokenize("( 2 )")))

    def test_rpn_value_parentheses_missing_right(self):
        calculator = Calculator()
        self.assertRaises(RuntimeError, calculator.to_rpn, calculator.tokenize("2 )"))

    def test_rpn_value_parentheses_missing_left(self):
        calculator = Calculator()
        self.assertRaises(RuntimeError, calculator.to_rpn, calculator.tokenize("( 2"))

    def test_rpn_decimal(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal("6.2"))
        ]
        self.assertListEqual(expected, calculator.to_rpn(calculator.tokenize("6.2")))

    def test_rpn_operator(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(2)),
            ValueToken(Decimal(4)),
            OperatorToken('+')
        ]
        self.assertListEqual(expected, calculator.to_rpn(calculator.tokenize("2 + 4")))

    def test_rpn_operator_parentheses(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(2)),
            ValueToken(Decimal(4)),
            OperatorToken('+'),
        ]
        self.assertListEqual(expected, calculator.to_rpn(calculator.tokenize("( 2 + 4 )")))

    def test_rpn_multiple_parentheses(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(3)),
            ValueToken(Decimal(2)),
            ValueToken(Decimal(4)),
            OperatorToken('+'),
            OperatorToken('*')
        ]
        self.assertListEqual(expected, calculator.to_rpn(calculator.tokenize("( 3 * ( ( 2 ) + ( 4 ) ) )")))

    def test_rpn_multiple_parentheses_decimal(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal("3.5")),
            ValueToken(Decimal("2.7")),
            ValueToken(Decimal("4.8")),
            OperatorToken('+'),
            OperatorToken('*')
        ]
        self.assertListEqual(expected, calculator.to_rpn(calculator.tokenize("( 3.5 * ( ( 2.7 ) + ( 4.8 ) ) )")))

    def test_rpn_operator_precedence(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(5)),
            ValueToken(Decimal(3)),
            ValueToken(Decimal(4)),
            OperatorToken('*'),
            OperatorToken('+')
        ]
        self.assertListEqual(expected, calculator.to_rpn(calculator.tokenize("5 + 3 * 4")))

    def test_rpn_operator_precedence_with_parentheses(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(5)),
            ValueToken(Decimal(3)),
            OperatorToken('+'),
            ValueToken(Decimal(4)),
            OperatorToken('*')
        ]
        self.assertListEqual(expected, calculator.to_rpn(calculator.tokenize("( 5 + 3 ) * 4")))

    def test_rpn_division(self):
        calculator = Calculator()
        expected = [
            ValueToken(Decimal(6)),
            ValueToken(Decimal(3)),
            OperatorToken('/')
        ]
        self.assertListEqual(expected, calculator.to_rpn(calculator.tokenize("6 / 3")))

if __name__ == '__main__':
    unittest.main()
