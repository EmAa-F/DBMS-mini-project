import tkinter as tk
from tkinter import ttk

from config.settings import (
    APP_TITLE, APP_WIDTH, APP_HEIGHT, MIN_WIDTH, MIN_HEIGHT,
    BG_SIDEBAR, BG_MAIN, BG_CARD, BORDER_COLOR,
    ACCENT_PRIMARY, ACCENT_SECONDARY, ACCENT_SUCCESS,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_HEADING, TEXT_ACCENT,
    FONT_FAMILY, FONT_TITLE, FONT_HEADING, FONT_SMALL,
)
from views.components import NavButton
from views.dashboard_view import DashboardView
from views.inventory_view import InventoryView
from views.alerts_view import AlertsView


class AppWindow:
    """
    Root application window.
    Manages sidebar navigation and view switching.
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(True, True)

        self._configure_styles()
        self._build_sidebar()
        self._build_content_area()

        self.show_dashboard()

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        # Treeview
        style.configure(
            "Dark.Treeview",
            background=BG_CARD,
            fieldbackground=BG_CARD,
            foreground=TEXT_PRIMARY,
            rowheight=32,
            font=(FONT_FAMILY, 10),
            borderwidth=0,
        )
        style.configure(
            "Dark.Treeview.Heading",
            background="#252837",
            foreground=TEXT_SECONDARY,
            font=(FONT_FAMILY, 9, "bold"),
            relief="flat",
            borderwidth=0,
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", ACCENT_PRIMARY)],
            foreground=[("selected", "#ffffff")],
        )

        # Combobox
        style.configure(
            "Dark.TCombobox",
            fieldbackground=BG_CARD,
            background=BG_CARD,
            foreground=TEXT_PRIMARY,
            arrowcolor=TEXT_SECONDARY,
            borderwidth=1,
            relief="flat",
        )
        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", BG_CARD)],
            foreground=[("readonly", TEXT_PRIMARY)],
        )

        # Scrollbar
        style.configure(
            "Dark.Vertical.TScrollbar",
            background=BG_CARD,
            troughcolor=BG_MAIN,
            borderwidth=0,
            arrowsize=0,
        )

    def _build_sidebar(self) -> None:
        sidebar = tk.Frame(self.root, bg=BG_SIDEBAR, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg=BG_SIDEBAR, pady=6)
        brand.pack(fill="x", padx=20, pady=(24, 4))

        tk.Label(
            brand, text="DS", font=(FONT_FAMILY, 20, "bold"),
            bg=BG_SIDEBAR, fg=ACCENT_PRIMARY,
        ).pack(side="left")

        brand_text = tk.Frame(brand, bg=BG_SIDEBAR)
        brand_text.pack(side="left", padx=(10, 0))
        tk.Label(
            brand_text, text="Dark Store", font=FONT_HEADING,
            fg=TEXT_HEADING, bg=BG_SIDEBAR,
        ).pack(anchor="w")
        tk.Label(
            brand_text, text="Inventory System", font=FONT_SMALL,
            fg=TEXT_SECONDARY, bg=BG_SIDEBAR,
        ).pack(anchor="w")

        tk.Frame(sidebar, bg=BORDER_COLOR, height=1).pack(
            fill="x", padx=16, pady=(20, 16)
        )

        tk.Label(
            sidebar, text="NAVIGATION", font=(FONT_FAMILY, 8, "bold"),
            fg=TEXT_SECONDARY, bg=BG_SIDEBAR, anchor="w",
        ).pack(fill="x", padx=24, pady=(0, 8))

        self.nav_buttons = {}

        self.nav_buttons["dashboard"] = NavButton(
            sidebar, "Dashboard", "", command=self.show_dashboard,
        )
        self.nav_buttons["dashboard"].pack(fill="x", pady=1)

        self.nav_buttons["inventory"] = NavButton(
            sidebar, "Inventory", "", command=self.show_inventory,
        )
        self.nav_buttons["inventory"].pack(fill="x", pady=1)

        self.nav_buttons["alerts"] = NavButton(
            sidebar, "Alerts", "", command=self.show_alerts,
        )
        self.nav_buttons["alerts"].pack(fill="x", pady=1)

        bottom = tk.Frame(sidebar, bg=BG_SIDEBAR)
        bottom.pack(side="bottom", fill="x", padx=20, pady=16)
        tk.Frame(bottom, bg=BORDER_COLOR, height=1).pack(fill="x", pady=(0, 12))
        tk.Label(
            bottom, text="NEP DBMS Project", font=FONT_SMALL,
            fg=TEXT_SECONDARY, bg=BG_SIDEBAR,
        ).pack(anchor="w")
        tk.Label(
            bottom, text="v2.0  •  SQLite + Tkinter", font=(FONT_FAMILY, 8),
            fg="#555870", bg=BG_SIDEBAR,
        ).pack(anchor="w", pady=(2, 0))

    def _build_content_area(self) -> None:
        self.content = tk.Frame(self.root, bg=BG_MAIN)
        self.content.pack(side="left", fill="both", expand=True)

    def _clear_content(self) -> None:
        for w in self.content.winfo_children():
            w.destroy()

    def _set_active_nav(self, key: str) -> None:
        for name, btn in self.nav_buttons.items():
            btn.set_active(name == key)

    def show_dashboard(self) -> None:
        self._set_active_nav("dashboard")
        self._clear_content()
        DashboardView(self.content)

    def show_inventory(self) -> None:
        self._set_active_nav("inventory")
        self._clear_content()
        InventoryView(self.content)

    def show_alerts(self) -> None:
        self._set_active_nav("alerts")
        self._clear_content()
        AlertsView(self.content)
