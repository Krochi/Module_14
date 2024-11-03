import sqlite3

def initiate_db():
    with sqlite3.connect("products.db") as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            description TEXT,
                            price INTEGER NOT NULL
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            email TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            balance INTEGER NOT NULL DEFAULT 1000
                        )''')
        connection.commit()

def populate_initial_products():
    with sqlite3.connect("products.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Products")
        count = cursor.fetchone()[0]

        if count == 0:
            products = [
                ("Product1", "Описание продукта 1", 100),
                ("Product2", "Описание продукта 2", 200),
                ("Product3", "Описание продукта 3", 300),
                ("Product4", "Описание продукта 4", 400)
            ]
            cursor.executemany("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", products)
            connection.commit()

def get_all_products():
    with sqlite3.connect("products.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
    return products

def add_user(username, email, age):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)", (username, email, age))
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users WHERE username = ?", (username,))
    exists = cursor.fetchone()[0] > 0
    connection.close()
    return exists


