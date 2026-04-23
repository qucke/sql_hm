import sqlite3
conn = sqlite3.connect("company.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Должности (
    Код_должности INTEGER PRIMARY KEY,
    Название TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Сотрудники (
    Код_сотрудника INTEGER PRIMARY KEY,
    Фамилия TEXT,
    Имя TEXT,
    Телефон TEXT,
    Код_должности INTEGER,
    FOREIGN KEY (Код_должности) REFERENCES Должности(Код_должности)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Клиенты (
    Код_клиента INTEGER PRIMARY KEY,
    Организация TEXT,
    Телефон TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Заказы (
    Код_заказа INTEGER PRIMARY KEY,
    Код_клиента INTEGER,
    Код_сотрудника INTEGER,
    Сумма REAL,
    Дата_выполнения TEXT,
    Отметка_о_выполнении INTEGER,
    FOREIGN KEY (Код_клиента) REFERENCES Клиенты(Код_клиента),
    FOREIGN KEY (Код_сотрудника) REFERENCES Сотрудники(Код_сотрудника)
)
""")

cursor.executemany("INSERT INTO Должности VALUES (?, ?)", [
    (1, 'Менеджер'),
    (2, 'Разработчик'),
    (3, 'Аналитик')
])

cursor.executemany("INSERT INTO Сотрудники VALUES (?, ?, ?, ?, ?)", [
    (1, 'Иванов', 'Иван', '111-111', 1),
    (2, 'Петров', 'Петр', '222-222', 2),
    (3, 'Сидоров', 'Сидор', '333-333', 3)
])

cursor.executemany("INSERT INTO Клиенты VALUES (?, ?, ?)", [
    (1, 'ООО Ромашка', '999-111'),
    (2, 'ЗАО Лотос', '999-222')
])

cursor.executemany("INSERT INTO Заказы VALUES (?, ?, ?, ?, ?, ?)", [
    (1, 1, 1, 10000, '2024-01-10', 1),
    (2, 2, 2, 20000, '2024-02-15', 1),
    (3, 1, 2, 15000, '2024-03-01', 0),
    (4, 2, 3, 5000, '2024-03-10', 1)
])

print("Количество сотрудников:")
cursor.execute("SELECT COUNT(*) FROM Сотрудники")
print(cursor.fetchone())

print("Максимальная сумма заказа:")
cursor.execute("SELECT MAX(Сумма) FROM Заказы")
print(cursor.fetchone())

print("Общая сумма заказов:")
cursor.execute("SELECT SUM(Сумма) FROM Заказы")
print(cursor.fetchone())

print("Средняя сумма:")
cursor.execute("SELECT AVG(Сумма) FROM Заказы")
print(cursor.fetchone())

print("Количество выполненных заказов:")
cursor.execute("SELECT COUNT(*) FROM Заказы WHERE Отметка_о_выполнении = 1")
print(cursor.fetchone())

print("Сумма заказов по клиентам:")
for row in cursor.execute("""
SELECT Код_клиента, SUM(Сумма)
FROM Заказы
GROUP BY Код_клиента
"""):
    print(row)

print("Количество заказов по сотрудникам:")
for row in cursor.execute("""
SELECT Код_сотрудника, COUNT(*)
FROM Заказы
GROUP BY Код_сотрудника
"""):
    print(row)

print("Средняя сумма по клиентам:")
for row in cursor.execute("""
SELECT Код_клиента, AVG(Сумма)
FROM Заказы
GROUP BY Код_клиента
"""):
    print(row)

print("Заказы с сотрудниками:")
for row in cursor.execute("""
SELECT Заказы.Код_заказа, Сотрудники.Фамилия, Заказы.Сумма
FROM Заказы
JOIN Сотрудники ON Заказы.Код_сотрудника = Сотрудники.Код_сотрудника
"""):
    print(row)

print("Выполненные заказы с клиентами:")
for row in cursor.execute("""
SELECT Заказы.Код_заказа, Клиенты.Организация, Заказы.Сумма
FROM Заказы
JOIN Клиенты ON Заказы.Код_клиента = Клиенты.Код_клиента
WHERE Заказы.Отметка_о_выполнении = 1
"""):
    print(row)

print("Сотрудники и должности:")
for row in cursor.execute("""
SELECT Сотрудники.Фамилия, Сотрудники.Имя, Должности.Название
FROM Сотрудники
JOIN Должности ON Сотрудники.Код_должности = Должности.Код_должности
"""):
    print(row)