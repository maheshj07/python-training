import sqlite3

DB_NAME = "inventory.db"


# 🔌 Get database connection
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# 🧱 Initialize database tables
def init_db():
    conn = get_db()
    cur = conn.cursor()

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # PRODUCTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)

    # ✅ Insert default admin user (safe check)
    cur.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", "admin")
        )

    # ✅ Insert sample products only if table is empty
    cur.execute("SELECT COUNT(*) as count FROM products")
    if cur.fetchone()["count"] == 0:
        products = [
            ("Laptop", "Computer", 55000, 5),
            ("Mouse", "Accessories", 500, 50),
            ("Keyboard", "Accessories", 1200, 8),
            ("Monitor", "Display", 12000, 3),
            ("Mobile Phone", "Electronics", 20000, 2),
        ]

        cur.executemany(
            "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
            products
        )

    conn.commit()
    conn.close()