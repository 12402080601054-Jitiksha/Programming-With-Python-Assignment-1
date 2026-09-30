# Exception-Safe CSV Transaction Splitter
# Assignment 1 - Question 4
# Python 3.10+

import csv
import os
from datetime import datetime


INPUT_FIELDS = [
    "transaction_id",
    "account_id",
    "type",
    "amount",
    "timestamp"
]

OUTPUT_FIELDS = [
    "transaction_id",
    "account_id",
    "type",
    "amount",
    "timestamp"
]


def validate_transaction(row, row_number):
    """
    Validate one transaction row.

    Returns:
        cleaned row if valid
        raises ValueError if invalid
    """

    # Check that all required fields are present.
    for field in INPUT_FIELDS:
        if field not in row:
            raise ValueError(
                f"Missing field: {field}"
            )

        if row[field] is None or not row[field].strip():
            raise ValueError(
                f"Empty field: {field}"
            )

    transaction_id = row["transaction_id"].strip()
    account_id = row["account_id"].strip()
    transaction_type = row["type"].strip().upper()
    amount_text = row["amount"].strip()
    timestamp = row["timestamp"].strip()

    # Validate transaction ID.
    if not transaction_id:
        raise ValueError("Invalid transaction_id")

    # Validate account ID.
    if not account_id:
        raise ValueError("Invalid account_id")

    # Validate transaction type.
    if transaction_type not in {"CREDIT", "DEBIT"}:
        raise ValueError(
            "type must be CREDIT or DEBIT"
        )

    # Validate amount.
    try:
        amount = float(amount_text)
    except ValueError:
        raise ValueError(
            "amount is not numeric"
        )

    if amount <= 0:
        raise ValueError(
            "amount must be greater than 0"
        )

    # Validate timestamp.
    try:
        datetime.strptime(
            timestamp,
            "%Y-%m-%dT%H:%M:%S"
        )
    except ValueError:
        raise ValueError(
            "invalid timestamp format"
        )

    return {
        "transaction_id": transaction_id,
        "account_id": account_id,
        "type": transaction_type,
        "amount": amount,
        "timestamp": timestamp
    }


def format_amount(amount):
    """
    Format amount so that integer values are printed
    without unnecessary decimal places.
    """
    if amount == int(amount):
        return str(int(amount))

    return f"{amount:.2f}"


def process_transactions(input_file):
    """
    Read the input CSV, validate transactions, write
    valid transactions to separate files, and write
    invalid rows to error.csv.
    """

    account_balances = {}

    with open(
        "credit.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as credit_file, \
    open(
        "debit.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as debit_file, \
    open(
        "error.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as error_file:

        credit_writer = csv.DictWriter(
            credit_file,
            fieldnames=OUTPUT_FIELDS
        )

        debit_writer = csv.DictWriter(
            debit_file,
            fieldnames=OUTPUT_FIELDS
        )

        error_writer = csv.writer(error_file)

        # Write headers.
        credit_writer.writeheader()
        debit_writer.writeheader()

        error_writer.writerow(
            INPUT_FIELDS + ["reason"]
        )

        try:
            with open(
                input_file,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                # Check input header.
                if reader.fieldnames != INPUT_FIELDS:
                    raise ValueError(
                        "Invalid CSV header"
                    )

                for row_number, row in enumerate(
                    reader,
                    start=2
                ):
                    try:
                        # Validate current transaction.
                        transaction = validate_transaction(
                            row,
                            row_number
                        )

                        transaction_type = transaction["type"]
                        amount = transaction["amount"]
                        account_id = transaction["account_id"]

                        # Write to appropriate output file.
                        if transaction_type == "CREDIT":
                            credit_writer.writerow(
                                transaction
                            )

                            account_balances[account_id] = (
                                account_balances.get(
                                    account_id,
                                    0
                                ) + amount
                            )

                        else:
                            debit_writer.writerow(
                                transaction
                            )

                            account_balances[account_id] = (
                                account_balances.get(
                                    account_id,
                                    0
                                ) - amount
                            )

                    except (ValueError, KeyError) as error:
                        # Invalid rows are written to error.csv.
                        original_values = [
                            row.get(field, "")
                            for field in INPUT_FIELDS
                        ]

                        error_writer.writerow(
                            original_values + [str(error)]
                        )

                        # Continue with the next row.

        except FileNotFoundError:
            print(
                f"Error: Input file '{input_file}' not found."
            )
            return None

        except PermissionError:
            print(
                "Error: Permission denied while accessing the file."
            )
            return None

    return account_balances


def display_summary(account_balances):
    """
    Display account-wise net balance changes in descending
    order of absolute balance change.
    """

    sorted_accounts = sorted(
        account_balances.items(),
        key=lambda item: (
            -abs(item[1]),
            item[0]
        )
    )

    print("Account-wise Net Balance Change:")

    for account_id, balance in sorted_accounts:
        print(
            f"{account_id} {format_amount(balance)}"
        )


def main():
    """Main program."""

    try:
        input_file = input(
            "Enter input CSV file path: "
        ).strip()

        if not input_file:
            print("Error: File path cannot be empty.")
            return

        if not os.path.isfile(input_file):
            print(
                f"Error: File '{input_file}' does not exist."
            )
            return

        account_balances = process_transactions(
            input_file
        )

        if account_balances is not None:
            display_summary(account_balances)

            print("\nFiles created:")
            print("credit.csv")
            print("debit.csv")
            print("error.csv")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()