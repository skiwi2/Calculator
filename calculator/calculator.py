from decimal import Decimal
from enum import Enum
import inspect
import re

from calculator.tokens import OperatorToken, ValueToken, LeftParenthesesToken, RightParenthesesToken


__author__ = 'Frank van Heeswijk'


class Associativity(Enum):
    left = 1
    right = 2


class Calculator:
    __operators = {
        # reference: http://en.wikipedia.org/wiki/Operators_in_C_and_C%2B%2B#Operator_precedence
        # operator: (precedence, associativity, function)
        "u+": (-3, Associativity.right, lambda op: op),
        "u-": (-3, Associativity.right, lambda op: -op),
        "*": (-5, Associativity.left, lambda op1, op2: op1 * op2),
        "/": (-5, Associativity.left, lambda op1, op2: op1 / op2),
        "+": (-6, Associativity.left, lambda op1, op2: op1 + op2),
        "-": (-6, Associativity.left, lambda op1, op2: op1 - op2)
    }

    def __init__(self):
        self.operators = Calculator.__operators

    def evaluate(self, expression: str) -> Decimal:
        """
        Evaluates an expression and returns its result.

        :param expression:  The input expression
        :return:    The output of evaluating the expression
        """

        tokens = self.to_rpn(self.tokenize(expression))
        stack = []
        for token in tokens:
            if isinstance(token, ValueToken):
                stack.append(token.value)
            elif isinstance(token, OperatorToken):
                function = self.operators[token.operator][2]
                argspec = inspect.getargspec(function)
                argument_count = len(argspec.args)

                if len(stack) < argument_count:
                    raise RuntimeError("not enough tokens for: " + str(token) + ", expected: " + str(argument_count) + ", actual: " + str(len(tokens)))
                values = [stack.pop() for x in range(argument_count)]
                values.reverse()
                result = function(*values)
                stack.append(result)
            else:
                raise RuntimeError("unexpected token: " + token)
        return stack.pop()

    def tokenize(self, expression: str) -> list:
        """
        Tokenizes an expression and produces an output list of tokens.

        :rtype: list of [Token]

        :param expression:  The input expression
        """

        # todo do not depend on spaces anymore
        raw_tokens = expression.split(' ')
        tokens = []

        decimal_regex = re.compile(r"^\d+(\.\d+)?$")

        for raw_token in raw_tokens:
            if decimal_regex.match(raw_token):
                tokens.append(ValueToken(Decimal(raw_token)))
            elif raw_token == '(':
                tokens.append(LeftParenthesesToken())
            elif raw_token == ')':
                tokens.append(RightParenthesesToken())
            else:
                if raw_token not in self.__operators:
                    raise RuntimeError("unsupported operator: " + raw_token)
                tokens.append(OperatorToken(raw_token))

        # resolve unary plus and minus operators
        for index, token in enumerate(tokens):
            if isinstance(token, OperatorToken) and token.operator == '-':
                if index == 0\
                or isinstance(tokens[index - 1], LeftParenthesesToken)\
                or isinstance(tokens[index - 1], OperatorToken):
                    tokens[index] = OperatorToken('u-')
            elif isinstance(token, OperatorToken) and token.operator == '+':
                if index == 0\
                or isinstance(tokens[index - 1], LeftParenthesesToken)\
                or isinstance(tokens[index - 1], OperatorToken):
                    tokens[index] = OperatorToken('u+')

        return tokens

    def to_rpn(self, tokens: list) -> list:
        """
        Converts a list of tokens to an output list in Reverse Polish Notation form.

        :rtype: list of [Token]

        :type tokens: list of [Token]

        :param tokens:  The input tokens
        :raise RuntimeError:    If the parentheses are mismatched
        """

        output_queue = []
        stack = []

        for token in tokens:
            if isinstance(token, ValueToken):
                output_queue.append(token)
            elif isinstance(token, LeftParenthesesToken):
                stack.append(token)
            elif isinstance(token, RightParenthesesToken):
                while len(stack) > 0:
                    pop_token = stack.pop()
                    if isinstance(pop_token, LeftParenthesesToken):
                        break
                    output_queue.append(pop_token)
                    # todo implement function support
                else:
                    raise RuntimeError("mismatched parentheses")
            elif isinstance(token, OperatorToken):
                while len(stack) > 0:
                    pop_token = stack.pop()
                    if isinstance(pop_token, OperatorToken) and self.__has_lower_precedence(token, pop_token):
                        output_queue.append(pop_token)
                    else:
                        stack.append(pop_token)
                        break
                stack.append(token)
            else:
                raise RuntimeError("unexpected token: " + token)

        while len(stack) > 0:
            pop_token = stack.pop()
            if isinstance(pop_token, LeftParenthesesToken):
                raise RuntimeError("mismatched parentheses")
            output_queue.append(pop_token)

        return output_queue

    def __has_lower_precedence(self, operatortoken1: OperatorToken, operatortoken2: OperatorToken) -> bool:
        operator1 = operatortoken1.operator
        operator2 = operatortoken2.operator
        if operator1 not in self.operators:
            raise RuntimeError("Unsupported operator token: " + operator1)
        if operator2 not in self.operators:
            raise RuntimeError("Unsupported operator token: " + operator2)
        operator1_tuple = self.operators[operator1]
        operator2_tuple = self.operators[operator2]
        return (operator1_tuple[1] == Associativity.left and operator1_tuple[0] <= operator2_tuple[0]) \
               or (operator1_tuple[1] == Associativity.right and operator1_tuple[0] < operator2_tuple[0])