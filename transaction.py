# The most Independent File

# Import Decimal for precise money values
from decimal import Decimal, InvalidOperation


# Define a class for one transaction
class Transaction:

    # Create a new transaction object
    def __init__(self, transaction_type, amount, category, description):

        # Clean and normalize transaction type
        self.transaction_type = transaction_type.strip().lower()

        # Ensure transaction type is valid
        if self.transaction_type not in ("income", "expense"):
            raise ValueError("Transaction type must be 'income' or 'expense'.")

        # Reject float explicitly because float is unsafe for money
        if isinstance(amount, float):
            raise TypeError("Float values are not allowed for money. Use a string, int, or Decimal.")

        # Try converting the amount into Decimal safely
        try:
            self.amount = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            raise ValueError("Amount must be a valid numeric value.")

        # Reject negative amounts
        if self.amount < 0:
            raise ValueError("Amount cannot be negative.")

        # Clean category text
        self.category = category.strip()

        # Ensure category is not empty
        if not self.category:
            raise ValueError("Category cannot be empty.")

        # Clean description text
        self.description = description.strip()

        # Ensure description is not empty
        if not self.description:
            raise ValueError("Description cannot be empty.")

    # Display one transaction in readable format
    def display(self):
        print(f"{self.transaction_type.title()}: ${self.amount:.2f} | {self.category} | {self.description}")