import tkinter as tk
from tkinter import ttk, messagebox

from config.settings import (
    BG_MAIN, BG_CARD, BG_INPUT, BORDER_COLOR,
    ACCENT_PRIMARY, ACCENT_SECONDARY, ACCENT_WARNING, ACCENT_SUCCESS,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_HEADING,
    FONT_FAMILY, FONT_HEADING, FONT_LABEL, FONT_BODY, FONT_SMALL, FONT_BUTTON,
    ALERT_COLUMNS, ALERT_WIDTHS,
    STOCK_CRITICAL,
)
from views.components import StyledButton, StatCard
from controllers.inventory_controller import get_alerts, stock_status


class AlertsView:
    """Builds the alerts view inside the given parent frame."""

    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        self._build()

    def _build(self) -> None:
        header = tk.Frame(self.parent, bg=BG_MAIN)
        header.pack(fill="x", padx=28, pady=(24, 4))

        tk.Label(header, text="Low Stock Alerts", font=(FONT_FAMILY, 18, "bold"),
                 fg=TEXT_HEADING, bg=BG_MAIN).pack(side="left")

        tk.Label(header, text="Items that need restocking",
                 font=FONT_BODY, fg=TEXT_SECONDARY, bg=BG_MAIN
                 ).pack(side="left", padx=(16, 0))

        self.cards_frame = tk.Frame(self.parent, bg=BG_MAIN)
        self.cards_frame.pack(fill="x", padx=24, pady=(16, 8))

        ctrl_frame = tk.Frame(self.parent, bg=BG_CARD, highlightthickness=1,
                               highlightbackground=BORDER_COLOR)
        ctrl_frame.pack(fill="x", padx=28, pady=(8, 8))
        ctrl_inner = tk.Frame(ctrl_frame, bg=BG_CARD, padx=16, pady=10)
        ctrl_inner.pack(fill="x")

        tk.Label(ctrl_inner, text="Alert Threshold", font=FONT_LABEL,
                 fg=TEXT_SECONDARY, bg=BG_CARD).pack(side="left")

        self.threshold_var = tk.StringVar(value="20")
        threshold_entry = tk.Entry(
            ctrl_inner, textvariable=self.threshold_var, width=6,
            font=FONT_LABEL, justify="center", bg=BG_INPUT, fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY, relief="flat",
            highlightthickness=1, highlightbackground=BORDER_COLOR,
            highlightcolor=ACCENT_PRIMARY,
        )
        threshold_entry.pack(side="left", padx=(10, 16), ipady=4)

        StyledButton(
            ctrl_inner, text="Scan", command=self._load_alerts,
            bg_color=ACCENT_SECONDARY, width=80, height=30,
        ).pack(side="left")

        tk.Label(ctrl_inner, text="Items with stock ≤ threshold will appear below",
                 font=FONT_SMALL, fg=TEXT_SECONDARY, bg=BG_CARD
                 ).pack(side="left", padx=(20, 0))

        table_frame = tk.Frame(self.parent, bg=BG_MAIN)
        table_frame.pack(fill="both", expand=True, padx=28, pady=(8, 4))

        self.tree = ttk.Treeview(
            table_frame, columns=ALERT_COLUMNS, show="headings",
            style="Dark.Treeview",
        )
        for col, w in zip(ALERT_COLUMNS, ALERT_WIDTHS):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center", minwidth=50)

        self.tree.tag_configure("critical", foreground=ACCENT_SECONDARY)
        self.tree.tag_configure("warning", foreground=ACCENT_WARNING)
        self.tree.tag_configure("healthy", foreground=ACCENT_SUCCESS)

        vsb = ttk.Scrollbar(table_frame, orient="vertical",
                             command=self.tree.yview,
                             style="Dark.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.pack(fill="both", expand=True)

        self.status_var = tk.StringVar(value="")
        tk.Label(self.parent, textvariable=self.status_var,
                 font=FONT_SMALL, fg=TEXT_SECONDARY, bg=BG_MAIN
                 ).pack(anchor="w", padx=28, pady=(4, 12))

        self._load_alerts()

    def _load_alerts(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            threshold = int(self.threshold_var.get())
        except ValueError:
            messagebox.showerror("Invalid", "Threshold must be a positive integer.")
            return

        rows = get_alerts(threshold)

        critical_count = 0
        warning_count = 0

        for row in rows:
            stock = row[4]
            status = stock_status(stock)
            if status == "critical":
                critical_count += 1
            elif status == "warning":
                warning_count += 1
            self.tree.insert("", "end", values=row, tags=(status,))

        for w in self.cards_frame.winfo_children():
            w.destroy()

        cards_data = [
            ("Total Alerts", len(rows), "", ACCENT_PRIMARY),
            ("Critical (≤10)", critical_count, "", ACCENT_SECONDARY),
            ("Warning (≤25)", warning_count, "", ACCENT_WARNING),
        ]
        for i, (title, value, icon, color) in enumerate(cards_data):
            card = StatCard(self.cards_frame, title, value, icon, color)
            card.grid(row=0, column=i, padx=6, pady=6, sticky="nsew")
            self.cards_frame.grid_columnconfigure(i, weight=1)

        self.status_var.set(
            f"{len(rows)} item(s) at or below threshold of {threshold}"
        )
