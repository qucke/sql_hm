import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.executescript("""
CREATE TABLE IF NOT EXISTS уровень_обучения (
    id_уровня INTEGER PRIMARY KEY,
    название TEXT
);

CREATE TABLE IF NOT EXISTS направления (
    id_направления INTEGER PRIMARY KEY,
    название TEXT
);

CREATE TABLE IF NOT EXISTS типы_обучения (
    id_типа INTEGER PRIMARY KEY,
    название TEXT
);

CREATE TABLE IF NOT EXISTS студенты (
    id_студента INTEGER PRIMARY KEY,
    id_уровня INTEGER,
    id_направления INTEGER,
    id_типа_обучения INTEGER,
    фамилия TEXT,
    имя TEXT,
    отчество TEXT,
    средний_балл REAL,
    FOREIGN KEY (id_уровня) REFERENCES уровень_обучения(id_уровня),
    FOREIGN KEY (id_направления) REFERENCES направления(id_направления),
    FOREIGN KEY (id_типа_обучения) REFERENCES типы_обучения(id_типа)
);
""")

conn.commit()
conn.close()