## Q3 - Recursive Expression Engine with Memoization

### Description
Evaluates integer expressions containing non-negative integers,
variables, +, -, *, and parentheses.

### Requirements
- Python 3.10 or above
- No external libraries required

### Data Structures
- Dictionary for variable definitions
- Dictionary for memoized results
- State dictionary for cycle detection
- Recursive parser for expressions

### Features
- Recursive expression evaluation
- Variable references
- Operator precedence
- Parentheses
- Memoization
- Cycle detection
- Invalid expression detection

### Classification
- Integer result: Valid expression
- CYCLE: Circular variable dependency detected
- INVALID: Invalid expression or undefined variable

### Run
python 12402080601054_Assignment1_Q3.py

### Time Complexity
O(total expression length)

### Space Complexity
O(total expression length)
