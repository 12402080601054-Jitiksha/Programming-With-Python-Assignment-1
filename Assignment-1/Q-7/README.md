# Q7 - Interactive Formula Validator with Custom Exceptions

## Problem Description

Build an interactive calculator that accepts formulas in the form:

operand operator operand

Operands can be integers, decimals, or previously stored variables.

The calculator also supports variable assignments such as:

x = 10

The program continues accepting input until the user enters:

quit

Invalid inputs are handled using separate custom exceptions.

---

## Custom Exceptions

The program uses the following custom exceptions:

### InvalidFormatError

Raised when the formula or assignment has an invalid format.

### UnknownVariableError

Raised when a variable is used before it has been defined.

### DivisionByZeroError

Raised when division or modulo by zero is attempted.

### UnsupportedOperatorError

Raised when an operator other than +, -, *, /, and % is used.

---

## Input Format

The program accepts multiple lines.

Examples:

x = 10

x + 5

x / 0

3 ** 2

quit

The program terminates when the user enters:

quit

---

## Output Format

For a valid formula, the calculated result is displayed.

For an invalid input, the corresponding exception type is displayed.

Example:

15

DivisionByZeroError

UnsupportedOperatorError

---

## Sample Input

x = 10
x + 5
x / 0
3 ** 2
quit

---

## Sample Output

15
DivisionByZeroError
UnsupportedOperatorError

---

## Features

- Interactive calculator
- Integer support
- Decimal support
- Variable storage
- Dictionary-based variable lookup
- Addition
- Subtraction
- Multiplication
- Division
- Modulo
- Custom exception handling
- Input validation
- Continues after errors
- Quit command

---

## Data Structure

A Python dictionary is used to store variables and their values.

Example:

{
    "x": 10,
    "y": 20
}

Dictionary lookup takes O(1) average time.

---

## Algorithm

1. Create an empty dictionary for variables.
2. Read one line from the user.
3. If the input is `quit`, terminate the program.
4. If the input contains `=`, treat it as a variable assignment.
5. Validate the variable name.
6. Store the calculated value in the dictionary.
7. Otherwise, treat the input as a formula.
8. Split the formula into operand, operator, and operand.
9. Validate the operator.
10. Resolve numeric values or stored variables.
11. Check for division or modulo by zero.
12. Perform the operation.
13. Print the result.
14. If an exception occurs, print the exception type and continue.
15. Repeat until `quit`.

---

## Example

Input:

x = 10

x + 5

Output:

15

---

## Error Example

Input:

x / 0

Output:

DivisionByZeroError

The program continues running after displaying the error.

---

## Complexity Analysis

### Time Complexity

O(1) average per formula.

Dictionary lookup takes O(1) average time.

### Space Complexity

O(v)

where v is the number of stored variables.

---

## How to Run

Python 3.10 or later is required.

Open the terminal in the folder containing the Python file.

Run:

python 12402080601054_Assignment1_Q7.py

The program will display:

Interactive Formula Calculator
Enter formulas one by one.
Examples: x = 10, x + 5, x / 2
Type 'quit' to exit.

Then enter formulas interactively.

---

## Test Cases

### Test Case 1 - Unknown Variable

Input:

abc + 10
quit

Expected Output:

UnknownVariableError
Calculator terminated.

---

### Test Case 2 - Invalid Format

Input:

10 +
quit

Expected Output:

InvalidFormatError
Calculator terminated.

---

## Learning Outcomes

After completing this program, the following concepts are demonstrated:

- Exception handling
- Custom exceptions
- Dictionaries
- Parsing input
- Arithmetic operations
- Variable management
- Input validation
- Interactive Python programs
- Object-oriented programming
- Time and space complexity
