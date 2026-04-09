import os
import sqlite3
import random
import sys


SCRIPTS_DIR  = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPTS_DIR)
DB_PATH      = os.path.join(PROJECT_ROOT, "data", "electronics_darkstore.db")

RANDOM_SEED = 42



CATEGORIES = [
    (1, "Laptops"),
    (2, "Phones"),
    (3, "Audio"),
    (4, "Tablets"),
    (5, "Gaming"),
]

SUPPLIERS = [
    (501, "Reliance Digital"),
    (502, "Croma Retail"),
    (503, "Amazon Wholesaler"),
]

STORES = [
    (10, "Mumbai-Andheri"),
    (20, "Bangalore-Whitefield"),
]

PRODUCT_BASE_NAMES = [
    "MacBook Pro", "iPhone 15", "Sony XM5", "iPad Air", "PS5 Console",
    "Dell XPS", "Samsung S24", "Bose QC45", "Surface Pro", "Xbox Series X",
    "HP Spectre", "Google Pixel 8", "Sennheiser HD", "Lenovo Yoga", "Nintendo Switch",
    "Asus ROG", "OnePlus 12", "JBL Flip 6", "Kindle Paperwhite", "GoPro Hero 12",
]



DROP_ORDER = [
    "Inventory", "StockAlerts", "Products",
    "Categories", "Suppliers", "Stores",
]

DDL = [
    "PRAGMA foreign_keys = ON",

    """CREATE TABLE IF NOT EXISTS Categories (
        cid   INT PRIMARY KEY,
        cname TEXT NOT NULL
    )""",

    """CREATE TABLE IF NOT EXISTS Suppliers (
        sup_id INT PRIMARY KEY,
        sname  TEXT NOT NULL
    )""",

    """CREATE TABLE IF NOT EXISTS Products (
        pid   INT  PRIMARY KEY,
        name  TEXT NOT NULL,
        cid   INT  NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (cid) REFERENCES Categories(cid)
    )""",

    """CREATE TABLE IF NOT EXISTS Stores (
        sid      INT  PRIMARY KEY,
        location TEXT NOT NULL
    )""",

    """CREATE TABLE IF NOT EXISTS Inventory (
        iid    INTEGER PRIMARY KEY AUTOINCREMENT,
        sid    INT NOT NULL,
        pid    INT NOT NULL,
        sup_id INT NOT NULL,
        stock  INT NOT NULL,
        FOREIGN KEY (sid)    REFERENCES Stores(sid),
        FOREIGN KEY (pid)    REFERENCES Products(pid),
        FOREIGN KEY (sup_id) REFERENCES Suppliers(sup_id)
    )""",

    """CREATE TABLE IF NOT EXISTS StockAlerts (
        alert_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        pid       INT NOT NULL,
        threshold INT NOT NULL DEFAULT 20,
        FOREIGN KEY (pid) REFERENCES Products(pid)
    )""",
]




def seed(db_path: str = DB_PATH) -> None:
    """Drop all tables, recreate them, and insert 50 products."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    rng = random.Random(RANDOM_SEED)
    conn = sqlite3.connect(db_path)

    try:
        cur = conn.cursor()

        for table in DROP_ORDER:
            cur.execute(f"DROP TABLE IF EXISTS {table}")

        for stmt in DDL:
            cur.execute(stmt)

        cur.executemany("INSERT INTO Categories VALUES (?,?)", CATEGORIES)
        cur.executemany("INSERT INTO Suppliers  VALUES (?,?)", SUPPLIERS)
        cur.executemany("INSERT INTO Stores     VALUES (?,?)", STORES)

        store_ids = [s[0] for s in STORES]
        sup_ids   = [s[0] for s in SUPPLIERS]
        cat_ids   = [c[0] for c in CATEGORIES]

        for i in range(1, 51):
            pid   = 1000 + i
            name  = f"{rng.choice(PRODUCT_BASE_NAMES)} Gen-{rng.randint(1, 5)}"
            cid   = rng.choice(cat_ids)
            price = rng.randint(15000, 150000)

            cur.execute(
                "INSERT INTO Products VALUES (?,?,?,?)",
                (pid, name, cid, price),
            )
            cur.execute(
                "INSERT INTO Inventory (sid, pid, sup_id, stock) VALUES (?,?,?,?)",
                (rng.choice(store_ids), pid, rng.choice(sup_ids), rng.randint(5, 100)),
            )

        conn.commit()
        print(f"Database seeded successfully at: {db_path}")
        print(f"   • {len(CATEGORIES)} categories")
        print(f"   • {len(SUPPLIERS)} suppliers")
        print(f"   • {len(STORES)} stores")
        print(f"   • 50 products with inventory")

    except Exception as e:
        conn.rollback()
        print(f"Seeding failed: {e}", file=sys.stderr)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    seed()
