import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import tkinter as tk
from config.settings import APP_TITLE
from models.database import db_exists, ensure_tables
from views.app_window import AppWindow


def main() -> None:
    """Initialize the database (if needed) and launch the GUI."""

    # Auto-seed if the database hasn't been created yet
    if not db_exists():
        print("Database not found — running initial seed...")
        from scripts.seed_db import seed
        seed()
        print()

    # Ensure supplementary tables exist
    ensure_tables()

    # Launch the application
    root = tk.Tk()
    AppWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
