import sys
from calculator.calculator import Calculator

__author__ = 'Frank van Heeswijk'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: calculator_application <expression>")
        sys.exit(1)
    calculator = Calculator()
    result = calculator.evaluate("".join(sys.argv[1:]))
    print(result)