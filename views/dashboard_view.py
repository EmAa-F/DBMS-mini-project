import tkinter as tk
from tkinter import ttk

from config.settings import (
    BG_MAIN, BG_CARD, BORDER_COLOR,
    ACCENT_PRIMARY, ACCENT_SECONDARY, ACCENT_SUCCESS, ACCENT_WARNING, ACCENT_INFO,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_HEADING,
    FONT_FAMILY, FONT_HEADING, FONT_LABEL, FONT_BODY, FONT_SMALL,
    FONT_CARD_NUM,
)
from views.components import SectionHeader, StatCard
from controllers.inventory_controller import get_dashboard_stats, format_price


class DashboardView:
    """Builds the dashboard view inside the given parent frame."""

    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        self.stats = get_dashboard_stats()
        self._build()

    def _build(self) -> None:
        canvas = tk.Canvas(self.parent, bg=BG_MAIN, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical",
                                   command=canvas.yview,
                                   style="Dark.Vertical.TScrollbar")
        self.frame = tk.Frame(canvas, bg=BG_MAIN)
        self.frame.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(-1 * (event.delta // 120), "units")
            except tk.TclError:
                pass
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self._build_header()
        self._build_stat_cards()
        self._build_store_breakdown()
        self._build_category_chart()

    def _build_header(self) -> None:
        header = tk.Frame(self.frame, bg=BG_MAIN)
        header.pack(fill="x", padx=28, pady=(24, 4))

        tk.Label(header, text="Dashboard", font=(FONT_FAMILY, 18, "bold"),
                 fg=TEXT_HEADING, bg=BG_MAIN).pack(side="left")

        tk.Label(header, text="Overview of your dark store inventory",
                 font=FONT_BODY, fg=TEXT_SECONDARY, bg=BG_MAIN
                 ).pack(side="left", padx=(16, 0))

    def _build_stat_cards(self) -> None:
        cards_frame = tk.Frame(self.frame, bg=BG_MAIN)
        cards_frame.pack(fill="x", padx=24, pady=(16, 8))

        cards_data = [
            ("Total Products", self.stats["total_products"], "", ACCENT_PRIMARY),
            ("Low Stock Items", self.stats["low_stock_count"], "", ACCENT_SECONDARY),
            ("Store Locations", self.stats["total_stores"], "", ACCENT_SUCCESS),
            ("Inventory Value", format_price(self.stats["total_inventory_value"]), "", ACCENT_INFO),
        ]

        for i, (title, value, icon, color) in enumerate(cards_data):
            card = StatCard(cards_frame, title, value, icon, color)
            card.grid(row=0, column=i, padx=6, pady=6, sticky="nsew")
            cards_frame.grid_columnconfigure(i, weight=1)

    def _build_store_breakdown(self) -> None:
        section = tk.Frame(self.frame, bg=BG_MAIN)
        section.pack(fill="x", padx=24, pady=(16, 8))

        tk.Label(section, text="Items per Store", font=FONT_HEADING,
                 fg=TEXT_HEADING, bg=BG_MAIN).pack(anchor="w", padx=6, pady=(0, 10))

        items_per_store = self.stats.get("items_per_store", {})
        total = sum(items_per_store.values()) if items_per_store else 1
        colors = [ACCENT_PRIMARY, ACCENT_SUCCESS, ACCENT_INFO, ACCENT_WARNING]

        for idx, (store, count) in enumerate(items_per_store.items()):
            row = tk.Frame(section, bg=BG_CARD, highlightthickness=1,
                          highlightbackground=BORDER_COLOR)
            row.pack(fill="x", padx=6, pady=3)

            inner = tk.Frame(row, bg=BG_CARD, padx=16, pady=12)
            inner.pack(fill="x")

            tk.Label(inner, text=store, font=FONT_LABEL,
                     fg=TEXT_PRIMARY, bg=BG_CARD).pack(side="left")
            tk.Label(inner, text=f"{count} items", font=FONT_BODY,
                     fg=TEXT_SECONDARY, bg=BG_CARD).pack(side="right")

            bar_bg = tk.Frame(row, bg="#252837", height=4)
            bar_bg.pack(fill="x", padx=16, pady=(0, 10))

            pct = count / total if total > 0 else 0
            bar_color = colors[idx % len(colors)]
            bar = tk.Frame(bar_bg, bg=bar_color, height=4)
            bar.place(relwidth=pct, relheight=1.0)

    def _build_category_chart(self) -> None:
        section = tk.Frame(self.frame, bg=BG_MAIN)
        section.pack(fill="x", padx=24, pady=(16, 24))

        tk.Label(section, text="Products by Category", font=FONT_HEADING,
                 fg=TEXT_HEADING, bg=BG_MAIN).pack(anchor="w", padx=6, pady=(0, 10))

        products_per_cat = self.stats.get("products_per_category", {})
        max_val = max(products_per_cat.values()) if products_per_cat else 1
        colors = [ACCENT_PRIMARY, ACCENT_SECONDARY, ACCENT_SUCCESS,
                  ACCENT_WARNING, ACCENT_INFO]

        grid_frame = tk.Frame(section, bg=BG_CARD, highlightthickness=1,
                              highlightbackground=BORDER_COLOR)
        grid_frame.pack(fill="x", padx=6)

        inner = tk.Frame(grid_frame, bg=BG_CARD, padx=16, pady=16)
        inner.pack(fill="x")

        for idx, (cat, count) in enumerate(products_per_cat.items()):
            row = tk.Frame(inner, bg=BG_CARD)
            row.pack(fill="x", pady=4)

            tk.Label(row, text=cat, font=FONT_BODY, fg=TEXT_PRIMARY,
                     bg=BG_CARD, width=12, anchor="w").pack(side="left")

            bar_container = tk.Frame(row, bg="#252837", height=20)
            bar_container.pack(side="left", fill="x", expand=True, padx=(8, 8))
            bar_container.pack_propagate(False)

            pct = count / max_val if max_val > 0 else 0
            bar = tk.Frame(bar_container, bg=colors[idx % len(colors)])
            bar.place(relwidth=pct, relheight=1.0)
            tk.Label(bar, text=str(count), font=FONT_SMALL,
                     fg="white", bg=colors[idx % len(colors)]).pack(
                         side="right", padx=6)

            tk.Label(row, text=str(count), font=FONT_SMALL,
                     fg=TEXT_SECONDARY, bg=BG_CARD).pack(side="left")

        summary = tk.Frame(inner, bg=BG_CARD)
        summary.pack(fill="x", pady=(12, 0))
        tk.Frame(summary, bg=BORDER_COLOR, height=1).pack(fill="x", pady=(0, 8))

        stats_info = [
            f"Avg Stock: {self.stats['avg_stock']}",
            f"Suppliers: {self.stats['total_suppliers']}",
            f"Categories: {self.stats['total_categories']}",
        ]
        for info in stats_info:
            tk.Label(summary, text=info, font=FONT_SMALL,
                     fg=TEXT_SECONDARY, bg=BG_CARD).pack(side="left", padx=(0, 20))
