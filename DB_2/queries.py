import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

print("Всего студентов:")
cursor.execute("SELECT COUNT(*) FROM студенты")
print(cursor.fetchone())

print("\nПо направлениям:")
for row in cursor.execute("""
SELECT направления.название, COUNT(*)
FROM студенты
JOIN направления ON студенты.id_направления = направления.id_направления
GROUP BY направления.название
"""):
    print(row)

print("\nПо типам обучения:")
for row in cursor.execute("""
SELECT типы_обучения.название, COUNT(*)
FROM студенты
JOIN типы_обучения ON студенты.id_типа_обучения = типы_обучения.id_типа
GROUP BY типы_обучения.название
"""):
    print(row)

print("\nСтатистика по направлениям:")
for row in cursor.execute("""
SELECT направления.название,
       MIN(средний_балл),
       MAX(средний_балл),
       AVG(средний_балл)
FROM студенты
JOIN направления ON студенты.id_направления = направления.id_направления
GROUP BY направления.название
"""):
    print(row)

print("\nСредний балл (направление + уровень + тип):")
for row in cursor.execute("""
SELECT н.название, у.название, т.название, AVG(средний_балл)
FROM студенты с
JOIN направления н ON с.id_направления = н.id_направления
JOIN уровень_обучения у ON с.id_уровня = у.id_уровня
JOIN типы_обучения т ON с.id_типа_обучения = т.id_типа
GROUP BY н.название, у.название, т.название
"""):
    print(row)

print("\nТОП-5 студентов:")
for row in cursor.execute("""
SELECT фамилия, имя, средний_балл
FROM студенты
JOIN направления ON студенты.id_направления = направления.id_направления
JOIN типы_обучения ON студенты.id_типа_обучения = типы_обучения.id_типа
WHERE направления.название = 'Прикладная информатика'
AND типы_обучения.название = 'Очная'
ORDER BY средний_балл DESC
LIMIT 5
"""):
    print(row)

print("\nОднофамильцы:")
for row in cursor.execute("""
SELECT фамилия, COUNT(*)
FROM студенты
GROUP BY фамилия
HAVING COUNT(*) > 1
"""):
    print(row)

print("\nПолные тезки:")
for row in cursor.execute("""
SELECT фамилия, имя, отчество, COUNT(*)
FROM студенты
GROUP BY фамилия, имя, отчество
HAVING COUNT(*) > 1
"""):
    print(row)

conn.close()