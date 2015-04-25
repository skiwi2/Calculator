from decimal import Decimal

__author__ = 'Frank van Heeswijk'


class Calculator:

    def evaluate(self, expression: str) -> Decimal:
        """
        Evaluates an expression and returns its result.

        :param expression:  The input string
        :return:    A decimal representing the string.
        """
        return Decimal(expression)