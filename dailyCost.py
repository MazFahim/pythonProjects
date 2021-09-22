# bismillahir rahmanir rahim
import datetime
import math
import sqlite3


def distribution(income):
    earning = 0
    dt = datetime.datetime.today()
    day = dt.day
    month = dt.month
    cursor.execute("SELECT * FROM account WHERE  month=?", (month,))
    rows = cursor.fetchall()
    for row in rows:
        if row[3] is None:
            continue
        else:
            earning = earning + row[3]

    income = income+earning
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        budget = income / 31
        b = math.floor(budget)
    elif month == 4 or month == 6 or month == 9 or month == 11:
        budget = income / 30
        b = math.floor(budget)
    else:
        budget = income / 28
        b = math.floor(budget)
    print("Your daily budget:", b)
    try:
        sqlite_insert_query = """INSERT INTO account
                              (day, month, income, budget) 
                               VALUES (?, ?, ?, ?);"""
        data = (day, month, income, b)
        cursor.execute(sqlite_insert_query, data)
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as e:
        print("Failed to insert data into sqlite table", e)
    # return b


def reserve(cost):
    dt = datetime.datetime.today()
    day = dt.day
    month = dt.month
    budget = 0
    savin = 0
    r = 0
    cursor.execute("SELECT * FROM account WHERE  month=?", (month,))
    rows = cursor.fetchall()
    for row in rows:
        if row[4] is None:
            pass
        else:
            budget = row[4]
        if row[6] is None:
            pass
        else:
            savin = row[6]
    s = budget - cost
    print("Your savings today:", s)
    savings = savin + s
    for row in rows:
        if row[1] == day:
            sql_update_query = """Update account set expense = ?, savings = ? where day = ?"""
            data = (cost, savings, day)
            cursor.execute(sql_update_query, data)
            sqliteConnection.commit()
            print("Record Updated successfully in the loop")
            r = 1
            cursor.close()
            break

    if r == 1:
        pass
    else:
        sqlite_insert_query = """INSERT INTO account
                                      (day, month, expense, savings) 
                                       VALUES (?, ?, ?, ?);"""
        data = (day, month, cost, savings)
        cursor.execute(sqlite_insert_query, data)
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()


def showAll():
    dt = datetime.datetime.today()
    day = dt.day
    month = dt.month
    cursor.execute("SELECT * FROM account where month=?", (month,))
    rows = cursor.fetchall()
    print("ID--Day---Month--Income--Budget--Expense--Savings")
    for row in rows:
        print(row[0], row[1], row[2], row[3], row[4], row[5], row[6])


try:
    sqliteConnection = sqlite3.connect('daily_cost.db')
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")

    sql = """ CREATE TABLE IF NOT EXISTS  account(
        id integer PRIMARY KEY,
        day string NOT NULL,
        month string NOT NULL,
        income integer,  
        budget integer,
        expense integer,
        savings integer
    );"""
    cursor.execute(sql)
    # print("Table created successfully........")

    # Commit your changes in the database
    sqliteConnection.commit()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

choice = int(input("Press 1 to enter income, press 2 to enter today's expense, press 3 to see your savings:"))
if choice == 1:
    earning = int(input("Enter the earning today:"))
    distribution(earning)
elif choice == 2:
    expense = int(input("Enter your today's expense:"))
    reserve(expense)
elif choice == 3:
    showAll()