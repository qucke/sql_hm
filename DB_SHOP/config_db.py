import sqlite3


def connect_db():
    conn = sqlite3.connect("shop.db")
    return conn


def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id_category INTEGER PRIMARY KEY AUTOINCREMENT,
        name_category TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id_product INTEGER PRIMARY KEY AUTOINCREMENT,
        name_of_product TEXT NOT NULL,
        price REAL NOT NULL,
        id_category INTEGER,
        quantity_at_storage INTEGER NOT NULL,
        FOREIGN KEY(id_category)
            REFERENCES categories(id_category)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS receipts (
        id_check INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sale_items (
        id_sale INTEGER PRIMARY KEY AUTOINCREMENT,
        id_check INTEGER,
        id_product INTEGER,
        quantity INTEGER NOT NULL,
        FOREIGN KEY(id_check)
            REFERENCES receipts(id_check),
        FOREIGN KEY(id_product)
            REFERENCES products(id_product)
    )
    """)

    conn.commit()
    conn.close()