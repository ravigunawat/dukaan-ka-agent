import sqlite3

DB_NAME = "dukaan.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT,
            price REAL,
            last_updated TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def update_stock(item, quantity, unit, price, action):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, quantity FROM stock WHERE item = ?", (item,))
    row = cursor.fetchone()

    if row:
        existing_id, existing_qty = row
        new_qty = existing_qty + quantity if action == "add" else existing_qty - quantity
        cursor.execute("UPDATE stock SET quantity = ?, price = ?, last_updated = CURRENT_TIMESTAMP WHERE id = ?",
                       (new_qty, price, existing_id))
    else:
        cursor.execute("INSERT INTO stock (item, quantity, unit, price) VALUES (?, ?, ?, ?)",
                       (item, quantity, unit, price))

    conn.commit()
    conn.close()

def get_all_stock():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT item, quantity, unit, price, last_updated FROM stock")
    rows = cursor.fetchall()
    conn.close()
    return [{"item": r[0], "quantity": r[1], "unit": r[2], "price": r[3], "last_updated": r[4]} for r in rows]
