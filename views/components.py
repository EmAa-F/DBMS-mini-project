import tkinter as tk
from config.settings import (
    BG_CARD, BG_INPUT, BG_SIDEBAR, BG_SIDEBAR_HL,
    ACCENT_PRIMARY, ACCENT_SUCCESS, ACCENT_WARNING, ACCENT_SECONDARY,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_HEADING,
    BORDER_COLOR,
    FONT_HEADING, FONT_LABEL, FONT_BODY, FONT_SMALL, FONT_BUTTON,
    FONT_CARD_NUM, FONT_FAMILY,
)


class StyledButton(tk.Canvas):
    """
    A modern flat button with rounded appearance, hover effects,
    and click animation.
    """

    def __init__(self, parent, text, command=None, bg_color=ACCENT_PRIMARY,
                 fg_color="white", width=120, height=34, font=FONT_BUTTON,
                 **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg=parent.cget("bg"), highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self._text = text
        self._font = font
        self._width = width
        self._height = height
        self._hover = False

        self._draw()
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _draw(self):
        self.delete("all")
        r = 6
        w, h = self._width, self._height
        color = self._lighten(self.bg_color, 20) if self._hover else self.bg_color

        self.create_rectangle(0, r, w, h - r, fill=color, outline="")

        self.create_text(w // 2, h // 2, text=self._text,
                         fill=self.fg_color, font=self._font)

    def _on_enter(self, _):
        self._hover = True
        self._draw()
        self.configure(cursor="hand2")

    def _on_leave(self, _):
        self._hover = False
        self._draw()

    def _on_press(self, _):
        self.move("all", 1, 1)

    def _on_release(self, _):
        self.move("all", -1, -1)
        if self.command:
            self.command()

    @staticmethod
    def _lighten(hex_color, amount):
        """Lighten a hex color by a given amount."""
        hex_color = hex_color.lstrip("#")
        r = min(255, int(hex_color[0:2], 16) + amount)
        g = min(255, int(hex_color[2:4], 16) + amount)
        b = min(255, int(hex_color[4:6], 16) + amount)
        return f"#{r:02x}{g:02x}{b:02x}"


class StatCard(tk.Frame):
    """
    A dashboard statistics card with an icon, value, and label.
    Features a subtle left-side accent bar.
    """

    def __init__(self, parent, title, value, icon="",
                 accent_color=ACCENT_PRIMARY, **kwargs):
        super().__init__(parent, bg=BG_CARD, highlightthickness=1,
                         highlightbackground=BORDER_COLOR, **kwargs)

        accent = tk.Frame(self, bg=accent_color, width=4)
        accent.pack(side="left", fill="y")

        content = tk.Frame(self, bg=BG_CARD, padx=16, pady=14)
        content.pack(side="left", fill="both", expand=True)

        top = tk.Frame(content, bg=BG_CARD)
        top.pack(fill="x")
        tk.Label(top, text=icon, font=(FONT_FAMILY, 14),
                 bg=BG_CARD, fg=TEXT_SECONDARY).pack(side="left")
        tk.Label(top, text=title, font=FONT_SMALL,
                 bg=BG_CARD, fg=TEXT_SECONDARY).pack(side="left", padx=(6, 0))

        self.value_label = tk.Label(content, text=str(value),
                                     font=FONT_CARD_NUM, bg=BG_CARD,
                                     fg=TEXT_HEADING, anchor="w")
        self.value_label.pack(fill="x", pady=(6, 0))

    def update_value(self, value):
        self.value_label.configure(text=str(value))


class NavButton(tk.Frame):
    """
    Sidebar navigation button with icon, text, active state indicator,
    and hover animation.
    """

    def __init__(self, parent, text, icon, command=None, **kwargs):
        super().__init__(parent, bg=BG_SIDEBAR, cursor="hand2", **kwargs)
        self.command = command
        self._active = False
        self._bg_normal = BG_SIDEBAR
        self._bg_hover = BG_SIDEBAR_HL
        self._bg_active = BG_SIDEBAR_HL

        self.configure(padx=0, pady=0)

        self.indicator = tk.Frame(self, bg=ACCENT_PRIMARY, width=3)

        self.content = tk.Frame(self, bg=self._bg_normal, padx=14, pady=10)
        self.content.pack(side="left", fill="both", expand=True)

        self.icon_label = tk.Label(self.content, text=icon,
                                    font=(FONT_FAMILY, 13),
                                    bg=self._bg_normal, fg=TEXT_SECONDARY)
        self.icon_label.pack(side="left")

        self.text_label = tk.Label(self.content, text=text, font=FONT_BODY,
                                    bg=self._bg_normal, fg=TEXT_SECONDARY)
        self.text_label.pack(side="left", padx=(10, 0))

        for widget in [self, self.content, self.icon_label, self.text_label]:
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<ButtonRelease-1>", self._on_click)

    def set_active(self, active: bool):
        self._active = active
        if active:
            self.indicator.pack(side="left", fill="y")
            bg = self._bg_active
            fg = TEXT_PRIMARY
        else:
            self.indicator.pack_forget()
            bg = self._bg_normal
            fg = TEXT_SECONDARY
        for w in [self, self.content, self.icon_label, self.text_label]:
            w.configure(bg=bg)
        self.icon_label.configure(fg=fg)
        self.text_label.configure(fg=fg)

    def _on_enter(self, _):
        if not self._active:
            bg = self._bg_hover
            for w in [self.content, self.icon_label, self.text_label]:
                w.configure(bg=bg)

    def _on_leave(self, _):
        if not self._active:
            bg = self._bg_normal
            for w in [self.content, self.icon_label, self.text_label]:
                w.configure(bg=bg)

    def _on_click(self, _):
        if self.command:
            self.command()


class SectionHeader(tk.Frame):
    """Dark header bar with title text for a content section."""

    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, bg=BG_CARD, **kwargs)
        self.configure(padx=24, pady=14)
        tk.Label(self, text=title, font=FONT_HEADING,
                 fg=TEXT_HEADING, bg=BG_CARD).pack(side="left")


class StyledEntry(tk.Frame):
    """An entry field with a dark background and subtle border."""

    def __init__(self, parent, textvariable=None, width=20,
                 placeholder="", **kwargs):
        super().__init__(parent, bg=BG_INPUT, highlightthickness=1,
                         highlightbackground=BORDER_COLOR,
                         highlightcolor=ACCENT_PRIMARY, **kwargs)

        self.entry = tk.Entry(
            self, textvariable=textvariable, width=width,
            font=FONT_BODY, bg=BG_INPUT, fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY, relief="flat",
            highlightthickness=0, border=0,
        )
        self.entry.pack(padx=8, pady=6)

        if placeholder:
            self._placeholder = placeholder
            self._has_placeholder = True
            self.entry.insert(0, placeholder)
            self.entry.configure(fg=TEXT_SECONDARY)
            self.entry.bind("<FocusIn>", self._clear_placeholder)
            self.entry.bind("<FocusOut>", self._set_placeholder)

    def _clear_placeholder(self, _):
        if self._has_placeholder:
            self.entry.delete(0, "end")
            self.entry.configure(fg=TEXT_PRIMARY)
            self._has_placeholder = False

    def _set_placeholder(self, _):
        if not self.entry.get():
            self.entry.insert(0, self._placeholder)
            self.entry.configure(fg=TEXT_SECONDARY)
            self._has_placeholder = True

    def get(self):
        if hasattr(self, "_has_placeholder") and self._has_placeholder:
            return ""
        return self.entry.get()
