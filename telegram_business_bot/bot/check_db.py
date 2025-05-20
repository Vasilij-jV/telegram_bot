from pathlib import Path
import sqlite3


def find_project_root(marker_files=(".env", "pyproject.toml", ".git")):
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if any((parent / marker).exists() for marker in marker_files):
            return parent
    raise RuntimeError("Не удалось найти корень проекта")


# Находим корень проекта
project_root = find_project_root()

# Путь к БД
db_path = project_root / "orders.db"  # Или .db, если это расширение у тебя

print(f"Путь к БД: {db_path}")

# Чтение данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Пример: вывод всех заказов
cursor.execute("SELECT * FROM orders")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
