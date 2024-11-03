import sqlite3

def initiate_db():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        price INTEGER NOT NULL
                    )''')
    connection.commit()
    connection.close()

def populate_initial_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Products")
    count = cursor.fetchone()[0]

    if count == 0:
        products = [
            ("Product1", "Описание продукта 1", 1000),
            ("Product2", "Описание продукта 2", 1200),
            ("Product3", "Описание продукта 3", 900),
            ("Product4", "Описание продукта 4", 1700)
        ]
        cursor.executemany("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", products)
        connection.commit()

    connection.close()

def get_all_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.close()
    return products
