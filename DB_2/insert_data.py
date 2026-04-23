import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.executemany("INSERT INTO уровень_обучения VALUES (?, ?)", [
    (1, "Бакалавр"),
    (2, "Магистр")
])

cursor.executemany("INSERT INTO направления VALUES (?, ?)", [
    (1, "Прикладная информатика"),
    (2, "Экономика")
])

cursor.executemany("INSERT INTO типы_обучения VALUES (?, ?)", [
    (1, "Очная"),
    (2, "Заочная"),
    (3, "Вечерняя")
])

cursor.executemany("INSERT INTO студенты VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [
    (1, 1, 1, 1, "Иванов", "Иван", "Иванович", 4.5),
    (2, 1, 1, 1, "Петров", "Петр", "Петрович", 4.8),
    (3, 2, 2, 2, "Сидоров", "Сидор", "Сидорович", 3.9),
    (4, 1, 1, 1, "Иванов", "Алексей", "Иванович", 4.9),
    (5, 1, 1, 1, "Смирнов", "Илья", "Игоревич", 5.0)
])

conn.commit()
conn.close()