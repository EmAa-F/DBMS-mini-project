import os


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR     = os.path.join(PROJECT_ROOT, "data")
DB_PATH      = os.path.join(DATA_DIR, "electronics_darkstore.db")


APP_TITLE  = "Electronics Dark Store — Inventory Tracker"
APP_WIDTH  = 1100
APP_HEIGHT = 700
MIN_WIDTH  = 900
MIN_HEIGHT = 580

BG_SIDEBAR     = "#0f1117"
BG_SIDEBAR_HL  = "#1a1d27"
BG_MAIN        = "#151821"
BG_CARD        = "#1c1f2e"
BG_HEADER      = "#1c1f2e"
BG_INPUT       = "#252837"
BG_TABLE_ROW   = "#1c1f2e"
BG_TABLE_ALT   = "#21243a"

ACCENT_PRIMARY   = "#6c63ff"
ACCENT_SECONDARY = "#ff6b6b"
ACCENT_SUCCESS   = "#2ed573"
ACCENT_WARNING   = "#ffa502"
ACCENT_INFO      = "#1e90ff"

TEXT_PRIMARY   = "#e8eaed"
TEXT_SECONDARY = "#8b8fa3"
TEXT_HEADING   = "#ffffff"
TEXT_ACCENT    = "#6c63ff"


BORDER_COLOR   = "#2a2d3e"
BORDER_RADIUS  = 8


FONT_FAMILY  = "Helvetica Neue"
FONT_TITLE   = (FONT_FAMILY, 16, "bold")
FONT_HEADING = (FONT_FAMILY, 13, "bold")
FONT_LABEL   = (FONT_FAMILY, 10, "bold")
FONT_BODY    = (FONT_FAMILY, 10)
FONT_SMALL   = (FONT_FAMILY, 9)
FONT_BUTTON  = (FONT_FAMILY, 10, "bold")
FONT_CARD_NUM = (FONT_FAMILY, 24, "bold")


INV_COLUMNS = ("ID", "Name", "Category", "Stock", "Price (₹)", "Supplier")
INV_WIDTHS  = (60, 200, 100, 70, 110, 150)

ALERT_COLUMNS = ("ID", "Name", "Category", "Store", "Stock", "Threshold")
ALERT_WIDTHS  = (60, 200, 100, 160, 70, 90)


STOCK_CRITICAL = 10
STOCK_WARNING  = 25
DEFAULT_ALERT_THRESHOLD = 20
