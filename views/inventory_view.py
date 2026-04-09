import tkinter as tk
from tkinter import ttk, messagebox

from config.settings import (
    BG_MAIN, BG_CARD, BG_INPUT, BORDER_COLOR,
    ACCENT_PRIMARY, ACCENT_SUCCESS, ACCENT_WARNING, ACCENT_SECONDARY,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_HEADING,
    FONT_FAMILY, FONT_HEADING, FONT_LABEL, FONT_BODY, FONT_SMALL,
    FONT_BUTTON, FONT_CARD_NUM,
    INV_COLUMNS, INV_WIDTHS,
    STOCK_CRITICAL, STOCK_WARNING,
)
from views.components import StyledButton, SectionHeader
from controllers.inventory_controller import (
    get_store_locations, get_categories, get_inventory,
    search_inventory, update_stock, format_price, stock_status,
)


class InventoryView:
    """Builds the inventory view inside the given parent frame."""

    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        self._build()

    def _build(self) -> None:
        header = tk.Frame(self.parent, bg=BG_MAIN)
        header.pack(fill="x", padx=28, pady=(24, 4))

        tk.Label(header, text="Inventory", font=(FONT_FAMILY, 18, "bold"),
                 fg=TEXT_HEADING, bg=BG_MAIN).pack(side="left")

        filter_frame = tk.Frame(self.parent, bg=BG_CARD, highlightthickness=1,
                                 highlightbackground=BORDER_COLOR)
        filter_frame.pack(fill="x", padx=28, pady=(16, 8))
        filter_inner = tk.Frame(filter_frame, bg=BG_CARD, padx=16, pady=12)
        filter_inner.pack(fill="x")

        filter_inner.pack(fill="x")

        tk.Label(filter_inner, text="Store", font=FONT_LABEL,
                 fg=TEXT_SECONDARY, bg=BG_CARD).pack(side="left")
        self.store_var = tk.StringVar()
        locations = get_store_locations()
        store_cb = ttk.Combobox(
            filter_inner, textvariable=self.store_var,
            values=locations, state="readonly", width=22,
            style="Dark.TCombobox",
        )
        store_cb.pack(side="left", padx=(8, 20))
        if locations:
            store_cb.current(0)

            store_cb.current(0)

        tk.Label(filter_inner, text="Category", font=FONT_LABEL,
                 fg=TEXT_SECONDARY, bg=BG_CARD).pack(side="left")
        self.cat_var = tk.StringVar(value="All")
        cat_cb = ttk.Combobox(
            filter_inner, textvariable=self.cat_var,
            values=["All"] + get_categories(), state="readonly", width=14,
            style="Dark.TCombobox",
        )
        cat_cb.pack(side="left", padx=(8, 20))

        cat_cb.pack(side="left", padx=(8, 20))

        tk.Label(filter_inner, text="Search:", font=(FONT_FAMILY, 12),
                 bg=BG_CARD, fg=TEXT_SECONDARY).pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            filter_inner, textvariable=self.search_var, width=18,
            font=FONT_BODY, bg=BG_INPUT, fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY, relief="flat",
            highlightthickness=1, highlightbackground=BORDER_COLOR,
            highlightcolor=ACCENT_PRIMARY,
        )
        search_entry.pack(side="left", padx=(6, 16), ipady=4)
        self.search_var.trace_add("write", lambda *_: self._on_search())

        StyledButton(
            filter_inner, text="Apply", command=self._load_data,
            bg_color=ACCENT_PRIMARY, width=80, height=30,
        ).pack(side="left")

        table_frame = tk.Frame(self.parent, bg=BG_MAIN)
        table_frame.pack(fill="both", expand=True, padx=28, pady=(8, 4))

        self.tree = ttk.Treeview(
            table_frame, columns=INV_COLUMNS, show="headings",
            style="Dark.Treeview",
        )
        for col, w in zip(INV_COLUMNS, INV_WIDTHS):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center", minwidth=50)

            self.tree.column(col, width=w, anchor="center", minwidth=50)

        self.tree.tag_configure("critical", foreground=ACCENT_SECONDARY)
        self.tree.tag_configure("warning", foreground=ACCENT_WARNING)
        self.tree.tag_configure("healthy", foreground=ACCENT_SUCCESS)
        self.tree.tag_configure("alt", background="#21243a")

        vsb = ttk.Scrollbar(table_frame, orient="vertical",
                             command=self.tree.yview,
                             style="Dark.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        bottom = tk.Frame(self.parent, bg=BG_MAIN, pady=8)
        bottom.pack(fill="x", padx=28)

        self.status_var = tk.StringVar(value="")
        tk.Label(bottom, textvariable=self.status_var, font=FONT_SMALL,
                 fg=TEXT_SECONDARY, bg=BG_MAIN).pack(side="left")

        StyledButton(
            bottom, text="Edit Stock", command=self._edit_stock,
            bg_color=ACCENT_SUCCESS, width=120, height=32,
        ).pack(side="right")

        self._load_data()

    def _load_data(self) -> None:
        """Load inventory data based on current filter selections."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        location = self.store_var.get()
        category = self.cat_var.get()

        if not location:
            return

        rows = get_inventory(location, category)
        for i, row in enumerate(rows):
            stock = row[3]
            status = stock_status(stock)
            tags = (status,)
            if i % 2:
                tags = (status, "alt")

            if i % 2:
                tags = (status, "alt")

            display_row = list(row)
            display_row[4] = format_price(row[4])
            self.tree.insert("", "end", values=display_row, tags=tags)

        self.status_var.set(f"{len(rows)} items found")

    def _on_search(self) -> None:
        """Real-time search filter."""
        term = self.search_var.get()
        location = self.store_var.get()
        if not location:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        if term.strip():
            rows = search_inventory(location, term)
        else:
            rows = get_inventory(location, self.cat_var.get())

        for i, row in enumerate(rows):
            stock = row[3]
            status = stock_status(stock)
            tags = (status,)
            if i % 2:
                tags = (status, "alt")

            display_row = list(row)
            display_row[4] = format_price(row[4])
            self.tree.insert("", "end", values=display_row, tags=tags)

        self.status_var.set(f"{len(rows)} items found")

    def _edit_stock(self) -> None:
        """Open a modal dialog to edit the stock of the selected item."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("No Selection",
                                "Select a row to edit its stock.")
            return

        values = self.tree.item(selected[0], "values")
        pid = int(values[0])
        name = values[1]
        current_stock = values[3]

        current_stock = values[3]

        win = tk.Toplevel(self.parent)
        win.title("Edit Stock")
        win.geometry("360x200")
        win.resizable(False, False)
        win.configure(bg=BG_CARD)
        win.grab_set()

        win.grab_set()

        win.transient(self.parent.winfo_toplevel())

        tk.Label(win, text="Edit Stock Quantity", font=FONT_HEADING,
                 fg=TEXT_HEADING, bg=BG_CARD).pack(pady=(20, 4))
        tk.Label(win, text=f"Product: {name}", font=FONT_BODY,
                 fg=TEXT_PRIMARY, bg=BG_CARD).pack()
        tk.Label(win, text=f"Current: {current_stock} units", font=FONT_SMALL,
                 fg=TEXT_SECONDARY, bg=BG_CARD).pack(pady=(2, 10))

        entry_var = tk.StringVar(value=str(current_stock))
        entry = tk.Entry(
            win, textvariable=entry_var, font=FONT_LABEL,
            justify="center", width=12, bg=BG_INPUT, fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY, relief="flat",
            highlightthickness=1, highlightbackground=BORDER_COLOR,
            highlightcolor=ACCENT_PRIMARY,
        )
        entry.pack(padx=40, ipady=6)
        entry.select_range(0, "end")
        entry.focus()

        def save():
            try:
                new_val = int(entry_var.get())
                update_stock(pid, new_val)
                win.destroy()
                self._load_data()
            except ValueError as e:
                messagebox.showerror(
                    "Invalid Input",
                    "Enter a valid non-negative integer.",
                    parent=win,
                )

        btn_frame = tk.Frame(win, bg=BG_CARD)
        btn_frame.pack(pady=14)
        StyledButton(
            btn_frame, text="Save", command=save,
            bg_color=ACCENT_SUCCESS, width=100, height=32,
        ).pack(side="left", padx=6)
        StyledButton(
            btn_frame, text="Cancel", command=win.destroy,
            bg_color="#555870", width=100, height=32,
        ).pack(side="left", padx=6)
