from decimal import Decimal

__author__ = 'Frank van Heeswijk'

class Calculator:

    def evaluate(self, expression):
        """
        Evaluates an expression and returns its result as a decimal.

        :param expression:  The input string
        :return:    A decimal representing the string.
        """
        return Decimal(expression)