import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

print("     CASE запросы     ")

print("\nКатегория студентов по среднему баллу:")
for row in cursor.execute("""
SELECT фамилия, имя, средний_балл,
CASE
    WHEN средний_балл >= 4.8 THEN 'Отличник'
    WHEN средний_балл >= 4.0 THEN 'Хорошист'
    ELSE 'Троечник'
END AS категория
FROM студенты
"""):
    print(row)

print("\nТип стипендии:")
for row in cursor.execute("""
SELECT фамилия, имя, средний_балл,
CASE
    WHEN средний_балл >= 4.8 THEN 'Повышенная'
    ELSE 'Обычная'
END AS стипендия
FROM студенты
"""):
    print(row)


print("\n    Подзапросы    ")

print("\nСтуденты выше среднего балла:")
for row in cursor.execute("""
SELECT фамилия, имя, средний_балл
FROM студенты
WHERE средний_балл > (
    SELECT AVG(средний_балл) FROM студенты
)
"""):
    print(row)

print("\nСтуденты с максимальным баллом:")
for row in cursor.execute("""
SELECT фамилия, имя, средний_балл
FROM студенты
WHERE средний_балл = (
    SELECT MAX(средний_балл) FROM студенты
)
"""):
    print(row)


print("\n    CTE    ")

print("\nСредний балл по направлениям:")
for row in cursor.execute("""
WITH avg_scores AS (
    SELECT id_направления, AVG(средний_балл) AS avg_ball
    FROM студенты
    GROUP BY id_направления
)
SELECT н.название, avg_scores.avg_ball
FROM avg_scores
JOIN направления н ON avg_scores.id_направления = н.id_направления
"""):
    print(row)

print("\nСтуденты выше среднего по своему направлению:")
for row in cursor.execute("""
WITH avg_scores AS (
    SELECT id_направления, AVG(средний_балл) AS avg_ball
    FROM студенты
    GROUP BY id_направления
)
SELECT с.фамилия, с.имя, с.средний_балл, н.название
FROM студенты с
JOIN avg_scores a ON с.id_направления = a.id_направления
JOIN направления н ON с.id_направления = н.id_направления
WHERE с.средний_балл > a.avg_ball
"""):
    print(row)

conn.close()
