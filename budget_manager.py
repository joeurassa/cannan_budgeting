# Second Most Independent File: Depends on Transaction.py File

from transaction import Transaction
# Import Decimal so totals also stay precise
from decimal import Decimal


# Define a class to manage all transactions
class BudgetManager:

    # Create a new budget manager with an empty transaction list
    def __init__(self):
        self.transactions = []

    # Add a transaction object to the system
    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    # Show all transactions
    def show_transactions(self):
        if not self.transactions:
            print("No transactions available.")
            return

        for index, transaction in enumerate(self.transactions, start=1):
            print(f"{index}. ", end="")
            transaction.display()

    # Calculate total income
    def get_total_income(self):
        total = Decimal("0.00")

        for transaction in self.transactions:
            if transaction.transaction_type == "income":
                total += transaction.amount

        return total

    # Calculate total expenses
    def get_total_expenses(self):
        total = Decimal("0.00")

        for transaction in self.transactions:
            if transaction.transaction_type == "expense":
                total += transaction.amount

        return total

    # Calculate current balance
    def get_balance(self):
        return self.get_total_income() - self.get_total_expenses()