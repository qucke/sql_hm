from datetime import datetime
from config_db import connect_db


def add_test_data():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO categories
    VALUES (1, 'Напитки')
    """)

    cur.execute("""
    INSERT OR IGNORE INTO categories
    VALUES (2, 'Сладости')
    """)

    cur.execute("""
    INSERT OR IGNORE INTO products
    VALUES (1, 'Кофе', 250, 1, 20)
    """)

    cur.execute("""
    INSERT OR IGNORE INTO products
    VALUES (2, 'Чай', 150, 1, 15)
    """)

    cur.execute("""
    INSERT OR IGNORE INTO products
    VALUES (3, 'Шоколад', 120, 2, 30)
    """)

    conn.commit()
    conn.close()


def get_products():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        p.id_product,
        p.name_of_product,
        c.name_category,
        p.price,
        p.quantity_at_storage
    FROM products p
    JOIN categories c
        ON p.id_category = c.id_category
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def make_purchase(cart):
    conn = connect_db()
    cur = conn.cursor()

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur.execute("""
    INSERT INTO receipts(created_at)
    VALUES (?)
    """, (current_date,))

    check_id = cur.lastrowid

    total_sum = 0

    for item in cart:
        product_id, price, quantity = item

        cur.execute("""
        INSERT INTO sale_items(
            id_check,
            id_product,
            quantity
        )
        VALUES (?, ?, ?)
        """, (check_id, product_id, quantity))

        cur.execute("""
        UPDATE products
        SET quantity_at_storage =
            quantity_at_storage - ?
        WHERE id_product = ?
        """, (quantity, product_id))

        total_sum += price * quantity

    conn.commit()
    conn.close()

    return check_id, total_sum


def get_report(date_value):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        p.name_of_product,
        SUM(s.quantity)
    FROM sale_items s
    JOIN products p
        ON s.id_product = p.id_product
    JOIN receipts r
        ON s.id_check = r.id_check
    WHERE date(r.created_at) = ?
    GROUP BY p.name_of_product
    """, (date_value,))

    sales = cur.fetchall()

    cur.execute("""
    SELECT
        SUM(s.quantity * p.price)
    FROM sale_items s
    JOIN products p
        ON s.id_product = p.id_product
    JOIN receipts r
        ON s.id_check = r.id_check
    WHERE date(r.created_at) = ?
    """, (date_value,))

    revenue = cur.fetchone()[0]

    conn.close()

    return sales, revenue