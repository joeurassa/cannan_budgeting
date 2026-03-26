# Second Most Independent File: Depends on Transaction.py File

from transaction import Transaction


class BudgetManager:
    def __init__(self):
        self.transactions = [] # create a list of transactions

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def show_transactions(self):
        if not self.transactions:
            print("No transactions available.")
            return

        for index, transaction in enumerate(self.transactions, start=1):
            print(f"{index}. ", end="")
            transaction.display() # summonig this from Transaction object method

    def get_total_income(self):
        total = 0
        for transaction in self.transactions:
            if transaction.transaction_type.lower() == "income":
                total += transaction.amount
        return total

    def get_total_expenses(self):
        total = 0
        for transaction in self.transactions:
            if transaction.transaction_type.lower() == "expense":
                total += transaction.amount
        return total

    def get_balance(self):
        return self.get_total_income() - self.get_total_expenses()