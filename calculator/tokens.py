from decimal import Decimal

__author__ = 'Frank van Heeswijk'


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


class RightParenthesesToken(Token):
    def __repr__(self):
        return "RPT"

    def __hash__(self):
        return 0

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return True

    def __ne__(self, other):
        return not self == other