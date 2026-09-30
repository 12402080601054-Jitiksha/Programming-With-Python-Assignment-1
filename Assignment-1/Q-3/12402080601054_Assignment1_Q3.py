# Recursive Expression Engine with Memoization
# Assignment 1 - Question 3
# Python 3.10+

import re


class ExpressionParser:
    """
    Recursive-descent parser for expressions containing:
    integers, variables, +, -, *, and parentheses.
    """

    def __init__(self, text, evaluator):
        self.text = text
        self.position = 0
        self.evaluator = evaluator

    def skip_spaces(self):
        """Skip whitespace characters."""
        while (
            self.position < len(self.text)
            and self.text[self.position].isspace()
        ):
            self.position += 1

    def parse(self):
        """Parse the complete expression."""
        value = self.parse_expression()

        self.skip_spaces()

        # All characters must be consumed.
        if self.position != len(self.text):
            raise ValueError("Invalid expression")

        return value

    def parse_expression(self):
        """
        expression = term ((+ | -) term)*
        """
        value = self.parse_term()

        while True:
            self.skip_spaces()

            if self.position >= len(self.text):
                break

            operator = self.text[self.position]

            if operator not in "+-":
                break

            self.position += 1
            right = self.parse_term()

            if operator == "+":
                value += right
            else:
                value -= right

        return value

    def parse_term(self):
        """
        term = factor (* factor)*
        """
        value = self.parse_factor()

        while True:
            self.skip_spaces()

            if self.position >= len(self.text):
                break

            if self.text[self.position] != "*":
                break

            self.position += 1
            right = self.parse_factor()

            value *= right

        return value

    def parse_factor(self):
        """
        factor = integer | variable | (expression)
        """
        self.skip_spaces()

        if self.position >= len(self.text):
            raise ValueError("Expected value")

        current = self.text[self.position]

        # Parenthesized expression
        if current == "(":
            self.position += 1

            value = self.parse_expression()

            self.skip_spaces()

            if (
                self.position >= len(self.text)
                or self.text[self.position] != ")"
            ):
                raise ValueError("Missing closing parenthesis")

            self.position += 1
            return value

        # Non-negative integer
        if current.isdigit():
            start = self.position

            while (
                self.position < len(self.text)
                and self.text[self.position].isdigit()
            ):
                self.position += 1

            return int(self.text[start:self.position])

        # Variable name
        if current.isalpha() or current == "_":
            start = self.position
            self.position += 1

            while self.position < len(self.text):
                ch = self.text[self.position]

                if ch.isalnum() or ch == "_":
                    self.position += 1
                else:
                    break

            variable_name = self.text[start:self.position]

            return self.evaluator.evaluate_variable(
                variable_name
            )

        raise ValueError("Invalid character")


class ExpressionEngine:
    """Stores variables and evaluates expressions."""

    def __init__(self, variables):
        self.variables = variables

        # Stores already calculated variable values.
        self.memo = {}

        # 0 = not being evaluated
        # 1 = currently being evaluated
        # 2 = completely evaluated
        self.state = {}

        self.cycle_found = False

    def evaluate_variable(self, name):
        """Evaluate a variable using recursion and memoization."""

        # Variable does not exist.
        if name not in self.variables:
            raise ValueError("Undefined variable")

        # Return previously calculated value.
        if name in self.memo:
            return self.memo[name]

        # Variable is already being evaluated.
        if self.state.get(name, 0) == 1:
            self.cycle_found = True
            raise RuntimeError("CYCLE")

        # Mark variable as currently being evaluated.
        self.state[name] = 1

        try:
            parser = ExpressionParser(
                self.variables[name],
                self
            )

            value = parser.parse()

            # Store result for future use.
            self.memo[name] = value

            # Mark as completely evaluated.
            self.state[name] = 2

            return value

        except RuntimeError:
            raise

        except ValueError:
            raise

    def evaluate(self, expression):
        """Evaluate the final expression."""

        parser = ExpressionParser(
            expression,
            self
        )

        return parser.parse()


def read_input():
    """Read variable definitions and final expression."""

    v_line = input().strip()

    if not v_line:
        raise ValueError("Invalid input")

    v = int(v_line)

    if not (1 <= v <= 200000):
        raise ValueError("Invalid number of variables")

    variables = {}

    for _ in range(v):
        line = input().strip()

        if "=" not in line:
            raise ValueError("Invalid variable definition")

        name, expression = line.split("=", 1)

        name = name.strip()
        expression = expression.strip()

        # Validate variable name.
        if not re.fullmatch(
            r"[A-Za-z_][A-Za-z0-9_]*",
            name
        ):
            raise ValueError("Invalid variable name")

        if not expression:
            raise ValueError("Empty expression")

        variables[name] = expression

    final_expression = input().strip()

    if not final_expression:
        raise ValueError("Empty final expression")

    return variables, final_expression


def main():
    try:
        variables, final_expression = read_input()

        engine = ExpressionEngine(variables)

        result = engine.evaluate(final_expression)

        print(result)

    except RuntimeError as error:
        if str(error) == "CYCLE":
            print("CYCLE")
        else:
            print("INVALID")

    except (ValueError, RecursionError):
        print("INVALID")


if __name__ == "__main__":
    main()