# Interactive Formula Validator with Custom Exceptions
# Assignment 1 - Question 7
# Python 3.10+

import re


# ---------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------

class FormulaError(Exception):
    """Base class for formula-related errors."""
    pass


class InvalidFormatError(FormulaError):
    """Raised when the formula format is invalid."""
    pass


class UnknownVariableError(FormulaError):
    """Raised when a variable is not defined."""
    pass


class DivisionByZeroError(FormulaError):
    """Raised when division or modulo by zero is attempted."""
    pass


class UnsupportedOperatorError(FormulaError):
    """Raised when an unsupported operator is used."""
    pass


# ---------------------------------------------------------
# Calculator Class
# ---------------------------------------------------------

class FormulaCalculator:
    """Interactive calculator for formulas and variables."""

    def __init__(self):
        # Dictionary to store variables and their values
        self.variables = {}

    def is_valid_variable_name(self, name):
        """
        Checks whether a variable name follows
        Python identifier rules.
        """
        return name.isidentifier()

    def parse_operand(self, operand):
        """
        Converts an operand into a number or retrieves
        its value from the variable dictionary.
        """

        # Check integer or decimal number
        try:
            return float(operand)
        except ValueError:
            pass

        # Check variable name
        if not self.is_valid_variable_name(operand):
            raise InvalidFormatError(
                "Invalid operand format."
            )

        # Check whether variable exists
        if operand not in self.variables:
            raise UnknownVariableError(
                f"Unknown variable: {operand}"
            )

        return self.variables[operand]

    def calculate(self, left, operator, right):
        """
        Performs the requested arithmetic operation.
        """

        if operator not in {"+", "-", "*", "/", "%"}:
            raise UnsupportedOperatorError(
                f"Unsupported operator: {operator}"
            )

        if operator in {"/", "%"} and right == 0:
            raise DivisionByZeroError(
                "Division by zero is not allowed."
            )

        if operator == "+":
            return left + right

        if operator == "-":
            return left - right

        if operator == "*":
            return left * right

        if operator == "/":
            return left / right

        if operator == "%":
            return left % right

    def evaluate_formula(self, formula):
        """
        Evaluates a formula of the form:

        operand operator operand
        """

        # Split formula using whitespace
        parts = formula.strip().split()

        # A valid formula must contain exactly 3 parts
        if len(parts) != 3:
            raise InvalidFormatError(
                "Formula must have the form: operand operator operand."
            )

        left_operand = parts[0]
        operator = parts[1]
        right_operand = parts[2]

        # Check operator before evaluating operands
        if operator not in {"+", "-", "*", "/", "%"}:
            raise UnsupportedOperatorError(
                f"Unsupported operator: {operator}"
            )

        left_value = self.parse_operand(left_operand)
        right_value = self.parse_operand(right_operand)

        return self.calculate(
            left_value,
            operator,
            right_value
        )

    def assign_variable(self, line):
        """
        Processes an assignment such as:

        x = 10
        y = x + 5
        """

        parts = line.split("=", 1)

        if len(parts) != 2:
            raise InvalidFormatError(
                "Invalid assignment format."
            )

        variable = parts[0].strip()
        value_expression = parts[1].strip()

        # Validate variable name
        if not variable or not self.is_valid_variable_name(variable):
            raise InvalidFormatError(
                "Invalid variable name."
            )

        # Assignment value can be a number
        # or a formula.
        value_parts = value_expression.split()

        if len(value_parts) == 1:
            value = self.parse_operand(value_parts[0])

        elif len(value_parts) == 3:
            value = self.evaluate_formula(value_expression)

        else:
            raise InvalidFormatError(
                "Invalid assignment expression."
            )

        self.variables[variable] = value

    def process_line(self, line):
        """
        Processes one line of user input.
        """

        line = line.strip()

        if not line:
            raise InvalidFormatError(
                "Input cannot be empty."
            )

        # Assignment statement
        if "=" in line:
            self.assign_variable(line)
            return None

        # Normal formula
        return self.evaluate_formula(line)


# ---------------------------------------------------------
# Helper Function
# ---------------------------------------------------------

def format_result(result):
    """
    Formats float results so that integers are displayed
    without unnecessary .0.
    """

    if result.is_integer():
        return str(int(result))

    return str(result)


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

def main():

    calculator = FormulaCalculator()

    print("Interactive Formula Calculator")
    print("Enter formulas one by one.")
    print("Examples: x = 10, x + 5, x / 2")
    print("Type 'quit' to exit.")
    print()

    while True:

        try:
            # Input prompt keeps the program waiting for user input
            line = input("> ").strip()

            # Exit condition
            if line.lower() == "quit":
                print("Calculator terminated.")
                break

            # Process input
            result = calculator.process_line(line)

            # Assignment does not print a result
            if result is not None:
                print(format_result(result))

        except FormulaError as error:

            # Print only the exception type as required
            print(type(error).__name__)

        except (ValueError, OverflowError):

            # Handles invalid numeric values
            print("InvalidFormatError")

        except KeyboardInterrupt:

            print("\nCalculator terminated.")
            break

        except EOFError:

            print("\nCalculator terminated.")
            break


# ---------------------------------------------------------
# Program Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()