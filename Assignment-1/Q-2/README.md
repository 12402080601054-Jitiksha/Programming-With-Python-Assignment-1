## Q2 - Optimized Password Audit with Pattern Constraints

### Description
Classifies candidate passwords as STRONG, WEAK_LENGTH,
WEAK_PATTERN, or COMPROMISED.

### Requirements
- Python 3.10 or above
- No external libraries required

### Data Structure
Aho-Corasick automaton based on Trie is used to efficiently
search for banned words.

### Validation Rules
- Password length must be 6 to 12.
- At least one lowercase letter.
- At least one uppercase letter.
- At least one digit.
- At least one special symbol from $, #, @.
- No character can repeat more than 3 consecutive times.
- Password must not contain a banned word, ignoring case.

### Run
python 12402080601054_Assignment1_Q2.py

### Time Complexity
O(B + P)

Where:
B = total length of banned words
P = total length of all passwords

### Space Complexity
O(B)
