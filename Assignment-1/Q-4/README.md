## Q4 - Exception-Safe CSV Transaction Splitter

### Description
Reads transaction records from a CSV file, validates each row,
separates valid credit and debit transactions, records invalid
rows with reasons, and calculates account-wise net balance changes.

### Requirements
- Python 3.10 or above
- No external libraries required

### Data Structures
- Dictionary for account-wise balance changes
- CSV reader and writer for file processing

### Validation
- Transaction ID cannot be empty.
- Account ID cannot be empty.
- Type must be CREDIT or DEBIT.
- Amount must be numeric and greater than 0.
- Timestamp must follow yyyy-mm-ddThh:mm:ss.

### Output Files
- credit.csv
- debit.csv
- error.csv

### Run
python 12402080601054_Assignment1_Q4.py

### Time Complexity
O(r + a log a)

### Space Complexity
O(a)
