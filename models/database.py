import sqlite3
from config.settings import DB_PATH




def _connect() -> sqlite3.Connection:
    """Return a new connection with foreign-key enforcement enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn




def ensure_tables() -> None:
    """Create the StockAlerts table if it does not already exist."""
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS StockAlerts (
                alert_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                pid       INT  NOT NULL,
                threshold INT  NOT NULL DEFAULT 20,
                FOREIGN KEY (pid) REFERENCES Products(pid)
            )
        """)
        conn.commit()


def db_exists() -> bool:
    """Check whether the database file has been seeded (Products table exists)."""
    try:
        with _connect() as conn:
            conn.execute("SELECT 1 FROM Products LIMIT 1")
        return True
    except Exception:
        return False




def get_store_locations() -> list[str]:
    """Return a sorted list of all store location names."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT location FROM Stores ORDER BY location"
        ).fetchall()
    return [r[0] for r in rows]


def get_categories() -> list[str]:
    """Return a sorted list of all category names."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT cname FROM Categories ORDER BY cname"
        ).fetchall()
    return [r[0] for r in rows]




def get_inventory_by_store(location: str, category: str = "All") -> list[tuple]:
    """
    Return inventory rows for a given store, optionally filtered by category.

    Columns: pid, product_name, category_name, stock, price, supplier_name
    Uses a 4-table JOIN: Inventory → Products → Categories → Stores → Suppliers.
    """
    base = """
        SELECT p.pid, p.name, c.cname, i.stock, p.price, sup.sname
        FROM  Inventory  i
        JOIN  Products   p   ON i.pid    = p.pid
        JOIN  Categories c   ON p.cid    = c.cid
        JOIN  Stores     s   ON i.sid    = s.sid
        JOIN  Suppliers  sup ON i.sup_id = sup.sup_id
        WHERE s.location = ?
    """
    if category != "All":
        base += " AND c.cname = ? ORDER BY c.cname, p.name"
        with _connect() as conn:
            return conn.execute(base, (location, category)).fetchall()
    base += " ORDER BY c.cname, p.name"
    with _connect() as conn:
        return conn.execute(base, (location,)).fetchall()


def search_inventory(location: str, search_term: str) -> list[tuple]:
    """
    Full-text search across product name, category, and supplier
    within a specific store.
    """
    query = """
        SELECT p.pid, p.name, c.cname, i.stock, p.price, sup.sname
        FROM  Inventory  i
        JOIN  Products   p   ON i.pid    = p.pid
        JOIN  Categories c   ON p.cid    = c.cid
        JOIN  Stores     s   ON i.sid    = s.sid
        JOIN  Suppliers  sup ON i.sup_id = sup.sup_id
        WHERE s.location = ?
          AND (   p.name   LIKE ?
               OR c.cname  LIKE ?
               OR sup.sname LIKE ?)
        ORDER BY c.cname, p.name
    """
    wildcard = f"%{search_term}%"
    with _connect() as conn:
        return conn.execute(
            query, (location, wildcard, wildcard, wildcard)
        ).fetchall()




def get_low_stock_items(threshold: int = 20) -> list[tuple]:
    """
    Return all items whose stock is at or below the given threshold.

    Columns: pid, product_name, category, store_location, stock, threshold
    """
    query = """
        SELECT p.pid, p.name, c.cname, s.location, i.stock, ? AS threshold
        FROM  Inventory  i
        JOIN  Products   p ON i.pid = p.pid
        JOIN  Categories c ON p.cid = c.cid
        JOIN  Stores     s ON i.sid = s.sid
        WHERE i.stock <= ?
        ORDER BY i.stock ASC
    """
    with _connect() as conn:
        return conn.execute(query, (threshold, threshold)).fetchall()




def get_dashboard_stats() -> dict:
    """
    Return aggregate statistics for the dashboard view.

    Keys: total_products, total_stores, total_categories, total_suppliers,
          total_inventory_value, low_stock_count, avg_stock, items_per_store
    """
    stats = {}
    with _connect() as conn:
        stats["total_products"] = conn.execute(
            "SELECT COUNT(*) FROM Products"
        ).fetchone()[0]

        stats["total_stores"] = conn.execute(
            "SELECT COUNT(*) FROM Stores"
        ).fetchone()[0]

        stats["total_categories"] = conn.execute(
            "SELECT COUNT(*) FROM Categories"
        ).fetchone()[0]

        stats["total_suppliers"] = conn.execute(
            "SELECT COUNT(*) FROM Suppliers"
        ).fetchone()[0]

        row = conn.execute("""
            SELECT COALESCE(SUM(i.stock * p.price), 0),
                   COALESCE(AVG(i.stock), 0)
            FROM Inventory i
            JOIN Products p ON i.pid = p.pid
        """).fetchone()
        stats["total_inventory_value"] = row[0]
        stats["avg_stock"] = round(row[1], 1)

        stats["low_stock_count"] = conn.execute(
            "SELECT COUNT(*) FROM Inventory WHERE stock <= 20"
        ).fetchone()[0]

        rows = conn.execute("""
            SELECT s.location, COUNT(i.iid) as cnt
            FROM Stores s
            LEFT JOIN Inventory i ON s.sid = i.sid
            GROUP BY s.location
            ORDER BY s.location
        """).fetchall()
        stats["items_per_store"] = {r[0]: r[1] for r in rows}

        cat_rows = conn.execute("""
            SELECT c.cname, COUNT(p.pid) as cnt
            FROM Categories c
            LEFT JOIN Products p ON c.cid = p.cid
            GROUP BY c.cname
            ORDER BY cnt DESC
        """).fetchall()
        stats["products_per_category"] = {r[0]: r[1] for r in cat_rows}

    return stats




def update_stock(pid: int, new_stock: int) -> None:
    """Update the stock quantity for a specific product in Inventory."""
    with _connect() as conn:
        conn.execute(
            "UPDATE Inventory SET stock = ? WHERE pid = ?",
            (new_stock, pid),
        )
        conn.commit()
