# Object-Oriented Bank Settlement System
# Assignment 1 - Question 5
# Python 3.10+

class BankException(Exception):
    """Base exception for bank-related errors."""
    pass


class AccountNotFoundException(BankException):
    """Raised when an account does not exist."""
    pass


class InvalidAmountException(BankException):
    """Raised when the transaction amount is invalid."""
    pass


class InsufficientBalanceException(BankException):
    """Raised when an account has insufficient balance."""
    pass


class InvalidOperationException(BankException):
    """Raised when an operation is invalid."""
    pass


class Account:
    """Represents a bank account."""

    def __init__(self, account_id, balance):
        if not account_id:
            raise ValueError("Account ID cannot be empty.")

        if balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        self._account_id = account_id
        self._balance = balance
        self._transaction_history = []

    # Getter for account ID
    @property
    def account_id(self):
        return self._account_id

    # Getter for balance
    @property
    def balance(self):
        return self._balance

    # Getter for transaction history
    @property
    def transaction_history(self):
        return self._transaction_history.copy()

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountException(
                "Amount must be greater than 0."
            )

        self._balance += amount
        self._transaction_history.append(
            ("DEPOSIT", amount)
        )

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountException(
                "Amount must be greater than 0."
            )

        if amount > self._balance:
            raise InsufficientBalanceException(
                "Insufficient balance."
            )

        self._balance -= amount
        self._transaction_history.append(
            ("WITHDRAW", amount)
        )


class Transaction:
    """Represents a bank transaction."""

    def __init__(
        self,
        operation,
        from_account=None,
        to_account=None,
        amount=None
    ):
        self.operation = operation
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount


class Bank:
    """Manages accounts and transactions."""

    def __init__(self):
        self._accounts = {}
        self._transaction_history = []

    def add_account(self, account):
        if account.account_id in self._accounts:
            raise InvalidOperationException(
                "Duplicate account ID."
            )

        self._accounts[account.account_id] = account

    def get_account(self, account_id):
        if account_id not in self._accounts:
            raise AccountNotFoundException(
                f"Account '{account_id}' not found."
            )

        return self._accounts[account_id]

    def validate_amount(self, amount):
        if amount <= 0:
            raise InvalidAmountException(
                "Amount must be greater than 0."
            )

        if amount > 1_000_000_000:
            raise InvalidAmountException(
                "Amount exceeds the allowed limit."
            )

    def deposit(self, account_id, amount):
        self.validate_amount(amount)

        account = self.get_account(account_id)

        account.deposit(amount)

        transaction = Transaction(
            "DEPOSIT",
            to_account=account_id,
            amount=amount
        )

        self._transaction_history.append(transaction)

    def withdraw(self, account_id, amount):
        self.validate_amount(amount)

        account = self.get_account(account_id)

        account.withdraw(amount)

        transaction = Transaction(
            "WITHDRAW",
            from_account=account_id,
            amount=amount
        )

        self._transaction_history.append(transaction)

    def transfer(self, from_id, to_id, amount):
        self.validate_amount(amount)

        if from_id == to_id:
            raise InvalidOperationException(
                "Source and destination cannot be the same."
            )

        from_account = self.get_account(from_id)
        to_account = self.get_account(to_id)

        if amount > from_account.balance:
            raise InsufficientBalanceException(
                "Insufficient balance."
            )

        # Perform transfer
        from_account.withdraw(amount)
        to_account.deposit(amount)

        transaction = Transaction(
            "TRANSFER",
            from_account=from_id,
            to_account=to_id,
            amount=amount
        )

        self._transaction_history.append(transaction)

    def create_snapshot(self):
        """
        Saves the current state of all accounts.
        Used for rollback.
        """
        snapshot = {}

        for account_id, account in self._accounts.items():
            snapshot[account_id] = (
                account.balance,
                len(account._transaction_history)
            )

        return snapshot

    def rollback(self, snapshot, history_length):
        """
        Restores all accounts and bank transaction history
        to the state before the batch started.
        """
        for account_id, state in snapshot.items():
            balance, transaction_count = state

            account = self._accounts[account_id]

            account._balance = balance

            account._transaction_history = (
                account._transaction_history[:transaction_count]
            )

        self._transaction_history = (
            self._transaction_history[:history_length]
        )

    def display_accounts(self):
        """Displays accounts in sorted account ID order."""
        for account_id in sorted(self._accounts):
            account = self._accounts[account_id]
            print(f"{account_id} {account.balance}")


def execute_operation(bank, parts):
    """Executes one transaction."""

    if not parts:
        raise InvalidOperationException(
            "Empty operation."
        )

    operation = parts[0]

    if operation == "DEPOSIT":

        if len(parts) != 3:
            raise InvalidOperationException(
                "Invalid DEPOSIT format."
            )

        account_id = parts[1]
        amount = int(parts[2])

        bank.deposit(account_id, amount)

    elif operation == "WITHDRAW":

        if len(parts) != 3:
            raise InvalidOperationException(
                "Invalid WITHDRAW format."
            )

        account_id = parts[1]
        amount = int(parts[2])

        bank.withdraw(account_id, amount)

    elif operation == "TRANSFER":

        if len(parts) != 4:
            raise InvalidOperationException(
                "Invalid TRANSFER format."
            )

        from_id = parts[1]
        to_id = parts[2]
        amount = int(parts[3])

        bank.transfer(from_id, to_id, amount)

    else:
        raise InvalidOperationException(
            f"Unknown operation: {operation}"
        )


def process_operations(bank, q):
    """
    Processes q operations.

    If any transaction inside a batch fails:
    - rollback the whole batch
    - ignore remaining transactions until BATCH_END
    - mark the batch as FAILED
    """

    inside_batch = False
    batch_failed = False

    batch_snapshot = None
    batch_history_length = 0

    batch_number = 0
    failed_batches = []

    for _ in range(q):

        operation_line = input().strip()

        if not operation_line:
            continue

        parts = operation_line.split()
        operation = parts[0]

        # -----------------------------
        # Start a new batch
        # -----------------------------
        if operation == "BATCH_BEGIN":

            if inside_batch:
                raise InvalidOperationException(
                    "Nested batches are not supported."
                )

            inside_batch = True
            batch_failed = False

            batch_number += 1

            # Save state before batch
            batch_snapshot = bank.create_snapshot()

            batch_history_length = len(
                bank._transaction_history
            )

            continue

        # -----------------------------
        # End current batch
        # -----------------------------
        if operation == "BATCH_END":

            if not inside_batch:
                raise InvalidOperationException(
                    "BATCH_END without BATCH_BEGIN."
                )

            # If the batch had failed,
            # report the failed batch.
            if batch_failed:
                failed_batches.append(batch_number)

            # Reset batch state
            inside_batch = False
            batch_failed = False
            batch_snapshot = None
            batch_history_length = 0

            continue

        # -----------------------------
        # If batch already failed,
        # ignore remaining operations
        # until BATCH_END.
        # -----------------------------
        if inside_batch and batch_failed:
            continue

        # -----------------------------
        # Execute normal operation
        # -----------------------------
        try:
            execute_operation(bank, parts)

        except (BankException, ValueError):

            if inside_batch:

                # Rollback entire batch
                bank.rollback(
                    batch_snapshot,
                    batch_history_length
                )

                # Mark batch as failed
                batch_failed = True

            else:
                # Operation outside a batch failed.
                # Ignore it and continue.
                continue

    # If input ends while a batch is still open,
    # rollback that incomplete batch.
    if inside_batch:

        bank.rollback(
            batch_snapshot,
            batch_history_length
        )

        if not batch_failed:
            batch_failed = True

        failed_batches.append(batch_number)

    return failed_batches


def main():

    try:

        # Number of accounts
        n = int(input().strip())

        if n < 1:
            raise ValueError(
                "Number of accounts must be positive."
            )

        bank = Bank()

        # Read accounts
        for _ in range(n):

            parts = input().strip().split()

            if len(parts) != 2:
                raise ValueError(
                    "Invalid account format."
                )

            account_id = parts[0]
            balance = int(parts[1])

            if balance < 0:
                raise ValueError(
                    "Initial balance cannot be negative."
                )

            bank.add_account(
                Account(account_id, balance)
            )

        # Number of operations
        q = int(input().strip())

        if q < 1:
            raise ValueError(
                "Number of operations must be positive."
            )

        # Process operations directly
        failed_batches = process_operations(
            bank,
            q
        )

        # Print failed batches
        for batch_number in failed_batches:
            print(f"FAILED {batch_number}")

        # Print final balances
        bank.display_accounts()

    except (ValueError, BankException) as error:

        print(f"INVALID {error}")

    except EOFError:

        print("INVALID")


if __name__ == "__main__":
    main()