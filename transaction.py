# The most Independent File


class Transaction:
    def __init__(self, transaction_type, amount, category, description):

        # validating transaction type, ensuring no mishandled data
        if transaction_type == "income" and amount < 0:
            raise ValueError("Income amount cannot be negative")



        self.transaction_type = transaction_type
        self.amount = amount
        self.category = category
        self.description = description

    def display(self):
        print(f"{self.transaction_type.title()}: ${self.amount:.2f} | {self.category} | {self.description}")