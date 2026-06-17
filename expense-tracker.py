expenses = []


def menu():
    print("\n--- EXPENSE TRACKER ---")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Show total")
    print("4. Exit")

def add_expense():
    amount = input("Enter amount: ")
    try:
        amount=int(amount)
        expenses.append(amount)
        print("Expense added successfully")
    except ValueError:
        print("invalid amount")

def view_expenses():
    if not expenses:
        print("no expenses found")
        return
    for expense in expenses:
        print(expense)

def show_total():
    total=sum(expenses)
    print(f"Total expenses: {total}")




while True:
    menu()
    option = input("Choose an option: ")

    if option == "1":
        add_expense()

    elif option == "2":
        view_expenses()

    elif option == "3":
        show_total()

    elif option == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid option")
