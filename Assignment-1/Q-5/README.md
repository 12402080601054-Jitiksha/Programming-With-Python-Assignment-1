## Q5 - Object-Oriented Bank Settlement System

### Description
An OOP-based bank settlement engine supporting deposits,
withdrawals, transfers, transaction history, overdraft
prevention, and atomic batch rollback.

### Requirements
- Python 3.10 or above
- No external libraries required

### Classes
- Account
- Transaction
- Bank

### Custom Exceptions
- BankException
- AccountNotFoundException
- InvalidAmountException
- InsufficientBalanceException
- InvalidOperationException

### Features
- Deposit
- Withdraw
- Transfer
- Transaction history
- Overdraft prevention
- Batch processing
- Complete batch rollback
- Final account sorting

### Run
python 12402080601054_Assignment1_Q5.py

### Time Complexity
O(q + n log n)

### Space Complexity
O(n + batch_size)
