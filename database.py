# database.py

import sqlite3
from datetime import datetime

# Инициализация базы данных SQLite
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            user_id INTEGER,
            amount REAL,
            date TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Добавление расхода в базу данных с текущей датой
def add_expense(user_id, amount):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d')  # Текущая дата
    cursor.execute('INSERT INTO expenses (user_id, amount, date) VALUES (?, ?, ?)', (user_id, amount, current_date))
    conn.commit()
    conn.close()

# Получение общей суммы расходов пользователя
def get_total_expenses(user_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ?', (user_id,))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0

# Получение расходов по месяцам
def get_monthly_expenses(user_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total
        FROM expenses
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month
    ''', (user_id,))
    monthly_expenses = cursor.fetchall()
    conn.close()
    return monthly_expenses