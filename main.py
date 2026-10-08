from database import get_connection
from expense import Expense
conn=get_connection()
print("successfully connected")
conn.close()

def create_table():
    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""
           CREATE TABLE IF NOT EXISTS users(

           id SERIAL PRIMARY KEY,
           username VARCHAR(255) UNIQUE NOT NULL,
           email VARCHAR(255) NOT NULL,
           password VARCHAR(255) NOT NULL)""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL)"""
    )


    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    amount NUMERIC(10,2) NOT NULL,
    description VARCHAR(255),
    categories_id INTEGER REFERENCES categories(id),
    date DATE NOT NULL DEFAULT CURRENT_DATE)""")






class User:
    def __init__(self,user_id,username,email):
        self.id=user_id
        self.name=username
        self.email=email


    @staticmethod
    def register(username,email,password):
            conn=get_connection()
            cur=conn.cursor()
            cur.execute(
               " INSERT INTO users(username,email,password) VALUES(%s,%s,%s) RETURNING id",
                (username,email,password)
            )
            user_id=cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return User(user_id,username,email)

    @staticmethod
    def login(username,password):
            conn=get_connection()
            cur=conn.cursor()
            cur.execute(
                "SELECT id,username,email FROM users WHERE username=%s AND password=%s",
                (username,password)
            )
            result=cur.fetchone()
            cur.close()
            conn.close()
            if result:
                return User(result[0],result[1],result[2])
            return None




def expense_menu(user):

    while True:
        print("\n========== EXPENSE TRACKER ==========")
        print(f"Welcome, {user.name}!")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")

        print("5. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            Expense.add_expense_menu(user.id)

        elif choice == "2":
            Expense.view_expenses(user.id)

        elif choice == "3":
            Expense.update_expense_menu(user.id)

        elif choice == "4":
            Expense.delete_expense_menu(user.id)

        elif choice == "5":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")



def main_menu():

        while True:

            print("\n========== EXPENSE TRACKER ==========")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

            choice = input("Choose an option: ")

            if choice == "1":

                username = input("Enter username: ")
                email = input("Enter email: ")
                password = input("Enter password: ")

                user = User.register(username, email, password)

                print(f"\nRegistration successful!")
                print(f"Your user ID is: {user.id}")

            elif choice == "2":

                username = input("Enter username: ")
                password = input("Enter password: ")

                user = User.login(username, password)

                if user:
                    print(f"\nLogin successful! Welcome, {user.name}!")
                    expense_menu(user)

                else:
                    print("\nInvalid username or password.")

            elif choice == "3":

                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")



main_menu()
