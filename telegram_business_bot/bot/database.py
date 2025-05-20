import sqlite3
import os
from pathlib import Path

# Путь к файлу БД — в корне проекта
# DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'orders.db'))
DB_PATH = Path(__file__).resolve().parent.parent / 'orders.db'


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                service TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


def save_order(name: str, phone: str, service: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (name, phone, service)
            VALUES (?, ?, ?)
        ''', (name, phone, service))
        conn.commit()


