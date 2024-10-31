import sqlite3 as sq

with sq.connect('not_telegram.db') as con:
    cursor = con.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INT NOT NULL,
balance INT NOT NULL
)
''')

users_db = [
    ('User1', 'example1@gmail.com', 10, 1000),
    ('User2', 'example2@gmail.com', 20, 1000),
    ('User3', 'example3@gmail.com', 30, 1000),
    ('User4', 'example4@gmail.com', 40, 1000),
    ('User5', 'example5@gmail.com', 50, 1000),
    ('User6', 'example6@gmail.com', 60, 1000),
    ('User7', 'example7@gmail.com', 70, 1000),
    ('User8', 'example8@gmail.com', 80, 1000),
    ('User9', 'example9@gmail.com', 90, 1000),
    ('User10', 'example10@gmail.com', 100, 1000)
]

cursor.executemany("INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?)", users_db)


#Обновите balance у каждой 2ой записи начиная с 1ой на 500:

cursor.execute("UPDATE Users SET balance=500 WHERE id % 2 = 0")


#Удалите каждую 3ую запись в таблице начиная с 1ой:

#cursor.execute("DELETE FROM Users WHERE id % 3 = 1")


#Сделайте выборку всех записей при помощи fetchall(), где возраст не равен 60

# cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60")
# result = cursor.fetchall()
# for username, email, age, balance in result:
#     print(f"Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}")

con.commit()
