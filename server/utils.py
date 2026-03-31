# Import Decimal to handle precise money values
# Import InvalidOperation to catch invalid number inputs
from decimal import Decimal, InvalidOperation


# Function to safely get a valid money amount from the user
def get_amount_input(prompt):

    # Keep asking until the user enters valid input
    while True:

        # Read input and remove spaces around it
        value = input(prompt).strip()

        # Reject empty input
        if not value:
            print("Amount cannot be empty.")
            continue

        # Try converting the input into Decimal
        try:
            amount = Decimal(value)
        except InvalidOperation:
            print("Invalid amount. Please enter a valid number like 10 or 19.99.")
            continue

        # Reject negative values
        if amount < 0:
            print("Amount cannot be negative.")
            continue

        # Reject values with more than 2 decimal places
        # Example: 10.999 should not be allowed as currency
        if amount.as_tuple().exponent < -2:
            print("Amount cannot have more than 2 decimal places.")
            continue

        # Optional: reject formats with unnecessary leading zeros
        # Examples rejected: 0005, 0012.50
        # Examples allowed: 0, 0.50, 10, 10.25
        if "." in value:
            whole_part = value.split(".")[0]
        else:
            whole_part = value

        # Remove optional plus sign before checking
        if whole_part.startswith("+"):
            whole_part = whole_part[1:]

        if len(whole_part) > 1 and whole_part.startswith("0"):
            print("Amount cannot contain unnecessary leading zeros.")
            continue

        # Return the cleaned original input
        return value



# Function to get a non-empty text input from the user
def get_non_empty_input(prompt):
    
    # Loop until valid input is provided
    while True:
        
        # Get input and remove leading/trailing spaces
        value = input(prompt).strip()

        # If input is empty, reject it
        if not value:
            print("This field cannot be empty.")
            continue  # Ask again

        # If valid, return the cleaned input
        return value


# Function to ensure user enters either "income" or "expense"
def get_transaction_type(prompt):
    
    # Loop until a valid type is entered
    while True:
        
        # Get input, remove spaces, and normalize to lowercase
        value = input(prompt).strip().lower()

        # Check if input is one of the allowed values
        if value in ("income", "expense"):
            return value  # Valid input

        # Otherwise, show error and repeat
        print("Invalid type. Enter 'income' or 'expense'.")