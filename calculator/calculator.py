from collections import deque
from decimal import Decimal
import re

__author__ = 'Frank van Heeswijk'


class Calculator:
    def evaluate(self, expression: str) -> Decimal:
        """
        Evaluates an expression and returns its result.

        :param expression:  The input expression
        :return:    The output of evaluating the expression
        """
        return Decimal(expression)

    def tokenize(self, expression: str) -> list:
        """
        Tokenizes an expression and produces an output list in Reverse Polish Notation form.

        :rtype: list of [Token]

        :param expression:  The input expression
        :raise RuntimeError:    If the parentheses are mismatched
        """
        output_queue = []
        stack = []
        # todo do not depend on spaces anymore
        tokens = expression.split(' ')

        decimal_regex = re.compile(r"^-?\d+(\.\d+)?$")

        for token in tokens:
            if decimal_regex.match(token):
                output_queue.append(ValueToken(Decimal(token)))
            elif token == '(':
                stack.append(LeftParenthesesToken())
            elif token == ')':
                while len(stack) > 0:
                    pop_token = stack.pop()
                    if isinstance(pop_token, LeftParenthesesToken):
                        break
                    output_queue.append(pop_token)
                    # todo implement function support
                else:
                    raise RuntimeError("mismatched parentheses")

            else:
                # todo implement precedence rules
                stack.append(OperatorToken(token))

        while len(stack) > 0:
            pop_token = stack.pop()
            if isinstance(pop_token, LeftParenthesesToken):
                raise RuntimeError("mismatched parentheses")
            output_queue.append(pop_token)

        return output_queue


class Token:
    pass


class ValueToken(Token):
    def __init__(self, value: Decimal):
        self.value = value

    def __repr__(self):
        return "VT(" + str(self.value) + ")"

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.value == other.value

    def __ne__(self, other):
        return not self == other


class OperatorToken(Token):
    def __init__(self, operator: str):
        self.operator = operator

    def __repr__(self):
        return "OT(" + self.operator + ")"

    def __hash__(self):
        return hash(str)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.operator == other.operator

    def __ne__(self, other):
        return not self == other

class LeftParenthesesToken(Token):
    def __repr__(self):
        return "LPT"

    def __hash__(self):
        return 0

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return True

    def __ne__(self, other):
        return not self == other