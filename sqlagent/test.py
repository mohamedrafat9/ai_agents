import sqlite3

connection = sqlite3.connect("sqlagent/db/database.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM customers;")

customers = cursor.fetchall()

for customer in customers:
    print(customer)

connection.close()