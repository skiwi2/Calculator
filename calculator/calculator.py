from decimal import Decimal

__author__ = 'Frank van Heeswijk'

class Calculator:

    def evaluate(self, expression):
        """
        Evauluates a string and returns a Decimal implementation thereof.

        :param expression:  The input string
        :return:    A decimal representing the string.
        """
        return Decimal(expression)