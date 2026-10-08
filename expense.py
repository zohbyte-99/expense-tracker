from database import get_connection
from categories import Category



class Expense:

    @staticmethod
    def add_expense(user_id, amount, description, category_id):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO expenses
            (user_id, amount, description, category_id,expense_date)
            VALUES (%s, %s, %s, %s,CURRENT_DATE)
            RETURNING id
        """, (user_id, amount, description, category_id))

        expense_id = cur.fetchone()[0]

        conn.commit()

        cur.close()
        conn.close()

        return expense_id

    @staticmethod
    def add_expense_menu(user_id):
        print("\n========== ADD EXPENSE ==========")

        amount = float(input("Enter amount: "))
        description = input("Enter description: ")

        Category.show_categories()

        category_id = int(input("Choose category: "))

        expense_id = Expense.add_expense(
            user_id,
            amount,
            description,
            category_id
        )

        print(f"\nExpense added successfully! ID: {expense_id}")

    @staticmethod
    def update_expense(user_id, expense_id, amount, description, category_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE expenses
            SET amount = %s,
                description = %s,
                category_id = %s
            WHERE id = %s AND user_id = %s
        """, (amount, description, category_id, expense_id, user_id))

        conn.commit()

        updated_rows = cur.rowcount

        cur.close()
        conn.close()

        return updated_rows

    @staticmethod
    def update_expense_menu(user_id):
        print("\n========== UPDATE EXPENSE ==========")

        Expense.view_expenses(user_id)

        expense_id = int(input("\nEnter the ID of the expense you want to update: "))

        amount = float(input("Enter new amount: "))
        description = input("Enter new description: ")

        Category.show_categories()
        category_id = int(input("Choose new category: "))

        updated = Expense.update_expense(
            user_id,
            expense_id,
            amount,
            description,
            category_id
        )

        if updated:
            print("\nExpense updated successfully!")
        else:
            print("\nExpense not found.")

    @staticmethod
    def delete_expense(user_id, expense_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM expenses
            WHERE id = %s AND user_id = %s
        """, (expense_id, user_id))

        conn.commit()

        deleted_rows = cur.rowcount

        cur.close()
        conn.close()

        return deleted_rows

    @staticmethod
    def delete_expense_menu(user_id):
        print("\n========== DELETE EXPENSE ==========")

        Expense.view_expenses(user_id)

        expense_id = int(input("\nEnter the ID of the expense you want to delete: "))

        deleted = Expense.delete_expense(user_id, expense_id)

        if deleted:
            print("\nExpense deleted successfully!")
        else:
            print("\nExpense not found.")

    @staticmethod
    def view_expenses(user_id):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                expenses.id,
                expenses.amount,
                expenses.description,
                categories.name,
                expenses.expense_date
            FROM expenses
            JOIN categories
                ON expenses.category_id = categories.id
            WHERE expenses.user_id = %s
            ORDER BY expenses.expense_date DESC
        """, (user_id,))

        expenses = cur.fetchall()

        cur.close()
        conn.close()

        if not expenses:
            print("\nYou have no expenses.")
            return

        print("\n========== YOUR EXPENSES ==========")
        print(f"{'ID':<5}{'Amount':<12}{'Description':<20}{'Category':<15}{'Date'}")
        print("-" * 70)

        for expense in expenses:
            print(
                f"{expense[0]:<5}"
                f"{expense[1]:<12}"
                f"{expense[2]:<20}"
                f"{expense[3]:<15}"
                f"{expense[4]}"
            )

