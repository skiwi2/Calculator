from decimal import Decimal
from enum import Enum
import re

from calculator.tokens import OperatorToken, ValueToken, LeftParenthesesToken


__author__ = 'Frank van Heeswijk'


class Associativity(Enum):
    left = 1
    right = 2


class Calculator:
    __operators = {
        # operator: (precedence, associativity, function)
        "+": (0, Associativity.left, lambda op1, op2: op1 + op2),
        "*": (1, Associativity.left, lambda op1, op2: op1 * op2)
    }

    def __init__(self):
        self.operators = Calculator.__operators

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
                while len(stack) > 0:
                    pop_token = stack.pop()
                    if isinstance(pop_token, OperatorToken) and self.__has_lower_precedence(token, pop_token.operator):
                        output_queue.append(pop_token)
                    else:
                        stack.append(pop_token)
                        break
                stack.append(self.__create_operator_token(token))

        while len(stack) > 0:
            pop_token = stack.pop()
            if isinstance(pop_token, LeftParenthesesToken):
                raise RuntimeError("mismatched parentheses")
            output_queue.append(pop_token)

        return output_queue

    def __create_operator_token(self, token: str) -> OperatorToken:
        if token in self.operators:
            return OperatorToken(token)
        raise RuntimeError("Unsupported operator token: " + token)

    def __has_lower_precedence(self, operator1: str, operator2: str) -> bool:
        if operator1 not in self.operators:
            raise RuntimeError("Unsupported operator token: " + operator1)
        if operator2 not in self.operators:
            raise RuntimeError("Unsupported operator token: " + operator2)
        operator1_tuple = self.operators[operator1]
        operator2_tuple = self.operators[operator2]
        return (operator1_tuple[1] == Associativity.left and operator1_tuple[0] <= operator2_tuple[0]) \
               or (operator1_tuple[1] == Associativity.right and operator1_tuple[0] < operator2_tuple[0])