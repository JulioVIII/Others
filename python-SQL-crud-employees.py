import sqlite3
import os

# The database file (company.db) will be created in the same folder as this Python script
print("Full path of the database:", os.path.abspath("company.db"))

# ===========================
# DATABASE CONNECTION & TABLE CREATION
# ===========================
def connect():
    return sqlite3.connect("company.db")  # DB will be created in the current folder

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL
        )
    """)
    conn.commit()
    # Insert a sample employee if table is empty
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)",
                       ("Laura Perez", "Analyst", 4200.50))
        conn.commit()
    conn.close()

# ===========================
# CRUD FUNCTIONS
# ===========================
def add_employee(name, position, salary):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)",
                   (name, position, salary))
    conn.commit()
    conn.close()
    print("✅ Employee added")

def list_employees():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()

    if employees:
        print("\n📋 Employees:")
        for emp in employees:
            print(f"ID:{emp[0]} Name:{emp[1]} Position:{emp[2]} Salary:{emp[3]}")
    else:
        print("No employees found")

def update_salary(employee_id, new_salary):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE employees SET salary=? WHERE id=?", (new_salary, employee_id))
    conn.commit()
    conn.close()
    print("✅ Salary updated")

def delete_employee(employee_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
    conn.commit()
    conn.close()
    print("✅ Employee deleted")

# ===========================
# INTERACTIVE MENU
# ===========================
def menu():
    create_table()  # Ensure the table exists and has at least one sample employee
    while True:
        print("\n=== MENU ===")
        print("1. Add employee")
        print("2. List employees")
        print("3. Update salary")
        print("4. Delete employee")
        print("5. Exit")

        option = input("Choose an option: ")

        if option == "1":
            name = input("Name: ")
            position = input("Position: ")
            salary = float(input("Salary: "))
            add_employee(name, position, salary)
        elif option == "2":
            list_employees()
        elif option == "3":
            list_employees()
            emp_id = int(input("Employee ID to update: "))
            new_salary = float(input("New salary: "))
            update_salary(emp_id, new_salary)
        elif option == "4":
            list_employees()
            emp_id = int(input("Employee ID to delete: "))
            delete_employee(emp_id)
        elif option == "5":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    menu()
