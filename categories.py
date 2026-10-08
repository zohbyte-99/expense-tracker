from database import get_connection


class Category:

    @staticmethod
    def get_categories():

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name
            FROM categories
            ORDER BY id
        """)

        categories = cur.fetchall()

        cur.close()
        conn.close()

        return categories

    @staticmethod
    def show_categories():

        categories = Category.get_categories()

        print("\nCategories:")

        for category in categories:
            print(f"{category[0]}. {category[1]}")

    @staticmethod
    def add_category(name):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO categories (name)
            VALUES (%s)
            RETURNING id
        """, (name,))

        category_id = cur.fetchone()[0]

        conn.commit()

        cur.close()
        conn.close()

        return category_id


