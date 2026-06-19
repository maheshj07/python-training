import sqlite3

DB = "inventory.db"

def connect():
    return sqlite3.connect(DB)

def create_tables():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price REAL,
    stock INTEGER,
    supplier TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    quantity INTEGER,
    total REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS suppliers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_sample_data():

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM products")

    if cur.fetchone()[0] == 0:

        products = [

        ("Dell Inspiron Laptop","Laptop",55000,15,"Dell"),
        ("HP 15s Laptop","Laptop",48000,8,"HP"),
        ("Lenovo IdeaPad","Laptop",50000,12,"Lenovo"),
        ("Samsung Galaxy A55","Mobile",32000,20,"Samsung"),
        ("iPhone 15","Mobile",79999,5,"Apple"),
        ("Boat Speaker","Accessories",2500,25,"Boat"),
        ("Sony Headphones","Accessories",4500,18,"Sony"),
        ("LG Smart TV","TV",42000,7,"LG"),
        ("Canon Printer","Printer",9500,9,"Canon"),
        ("Logitech Mouse","Accessories",1200,30,"Logitech")

        ]

        cur.executemany("""
        INSERT INTO products
        (name,category,price,stock,supplier)
        VALUES(?,?,?,?,?)
        """,products)

    conn.commit()
    conn.close()

def get_products():

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM products")

    data = cur.fetchall()

    conn.close()

    return data

def search_product(keyword):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM products WHERE name LIKE ?",
        ('%'+keyword+'%',)
    )

    data = cur.fetchall()

    conn.close()

    return data

def filter_products(category):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM products WHERE category=?",
        (category,)
    )

    data = cur.fetchall()

    conn.close()

    return data

def low_stock_products():

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM products WHERE stock < 10"
    )

    data = cur.fetchall()

    conn.close()

    return data

def get_suppliers():

    return [
        ("Dell","9876543210"),
        ("HP","9876543211"),
        ("Samsung","9876543212"),
        ("LG","9876543213")
    ]