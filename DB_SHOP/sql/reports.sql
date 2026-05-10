CREATE TABLE categories (
    id_category INTEGER PRIMARY KEY AUTOINCREMENT,
    name_category TEXT NOT NULL
);

CREATE TABLE products (
    id_product INTEGER PRIMARY KEY AUTOINCREMENT,
    name_of_product TEXT NOT NULL,
    price REAL NOT NULL,
    id_category INTEGER,
    quantity_at_storage INTEGER NOT NULL
);

CREATE TABLE receipts (
    id_check INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL
);

CREATE TABLE sale_items (
    id_sale INTEGER PRIMARY KEY AUTOINCREMENT,
    id_check INTEGER,
    id_product INTEGER,
    quantity INTEGER NOT NULL
);