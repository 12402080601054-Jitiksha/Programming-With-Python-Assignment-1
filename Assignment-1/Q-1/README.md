# Programming with Python - Assignment 1

## Q1 - Campus Merit Analyzer

### Python Version
Python 3.10 or above

### Description
The program analyzes student records using lists, tuples and dictionaries.

It displays:
- Top K students semester-wise
- Subject-wise toppers

### Ranking Criteria

Students are ranked using:

1. Higher CPI
2. Higher average marks when CPI is equal
3. Lexicographically smaller enrollment number when both CPI and average marks are equal

### Data Structures

- List - stores student records
- Tuple - stores immutable student records and marks
- Dictionary - groups students by semester

### How to Run

Open Command Prompt in the project folder and run:

python 12402080601054_Assignment1_Q1.py

### Input Format

n k m

enrollment name semester cpi mark1 mark2 ... markm

### Sample Input

5 2 3
2201 Asha 5 8.90 90 82 75
2202 Bharat 5 8.90 88 95 70
2203 Chaitra 3 9.10 91 88 92
2204 Dev 5 7.80 76 80 85
2205 Esha 3 9.10 91 90 88

### Expected Output

Semester 3: 2205 2203
Semester 5: 2202 2201
S1: 2203 2205
S2: 2202
S3: 2203

### Complexity

Time Complexity:
O(n*m + n log n)

Space Complexity:
O(n*m)

### Testing

The program was tested using:

- Official sample test
- Boundary test
- Three self-created test cases
- Invalid input tests
