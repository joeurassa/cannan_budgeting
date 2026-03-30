# this is the main file
# Date Created: March 26, 2026
# Author      : Joseph Urassa
# 'Inspired by new friend Cannan Murphy.

# Import your modules
from transaction import Transaction
from budget_manager import BudgetManager
from utils import get_amount_input, get_non_empty_input, get_transaction_type

2
# Function to collect user input and create a Transaction
def get_transaction_input():
    transaction_type = get_transaction_type("Enter transaction type (income/expense): ")
    amount = get_amount_input("Enter amount: ")
    category = get_non_empty_input("Enter category: ")
    description = get_non_empty_input("Enter description: ")

    return Transaction(transaction_type, amount, category, description)


# Main program loop
def main():
    manager = BudgetManager()

    while True:
        print("\n--- Budget Manager ---")
        print("1. Add Transaction")
        print("2. Show Transactions")
        print("3. Show Summary")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                transaction = get_transaction_input()
                manager.add_transaction(transaction)
                print("Transaction added successfully.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            manager.show_transactions()

        elif choice == "3":
            print(f"Total Income: ${manager.get_total_income():.2f}")
            print(f"Total Expenses: ${manager.get_total_expenses():.2f}")
            print(f"Balance: ${manager.get_balance():.2f}")

        elif choice == "4":
            print("Exiting program.")
            break

        else:
            print("Invalid choice.")


# This ensures the program runs only when this file is executed directly
if __name__ == "__main__":
    main()


