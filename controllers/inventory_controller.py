from models import database


def get_store_locations() -> list[str]:
    """Fetch all store locations for UI dropdowns."""
    return database.get_store_locations()


def get_categories() -> list[str]:
    """Fetch all category names for UI dropdowns."""
    return database.get_categories()


def get_inventory(location: str, category: str = "All") -> list[tuple]:
    """Fetch inventory rows, optionally filtered by category."""
    return database.get_inventory_by_store(location, category)


def search_inventory(location: str, term: str) -> list[tuple]:
    """Search inventory by name, category, or supplier."""
    if not term.strip():
        return database.get_inventory_by_store(location)
    return database.search_inventory(location, term.strip())


def get_alerts(threshold: int = 20) -> list[tuple]:
    """Fetch low-stock items at or below the given threshold."""
    return database.get_low_stock_items(threshold)


def get_dashboard_stats() -> dict:
    """Fetch aggregate dashboard statistics."""
    return database.get_dashboard_stats()


def update_stock(pid: int, new_stock: int) -> bool:
    """
    Validate and update stock for a product.
    Returns True on success, raises ValueError on bad input.
    """
    if new_stock < 0:
        raise ValueError("Stock cannot be negative.")
    database.update_stock(pid, new_stock)
    return True


def format_price(price: float) -> str:
    """Format a price in Indian Rupee notation (e.g. ₹1,25,000)."""
    price_int = int(price)
    s = str(price_int)
    if len(s) <= 3:
        return f"₹{s}"
    # Indian grouping: last 3 digits, then groups of 2
    last3 = s[-3:]
    rest = s[:-3]
    groups = []
    while rest:
        groups.insert(0, rest[-2:])
        rest = rest[:-2]
    return "₹" + ",".join(groups) + "," + last3


def stock_status(stock: int) -> str:
    """Return a status label based on stock level."""
    if stock <= 10:
        return "critical"
    elif stock <= 25:
        return "warning"
    else:
        return "healthy"
