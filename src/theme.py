"""
theme.py - Centralized design tokens for Instagram Red Flags.
"""


class Colors:
    """Dark mode palette with blue accents."""

    BG_DARKEST = "#0B0E17"
    BG_DARK = "#111827"
    BG_CARD = "#1A2236"
    BG_CARD_ALT = "#1E293B"
    BG_HOVER = "#253352"

    ACCENT_PRIMARY = "#3B82F6"
    ACCENT_HOVER = "#2563EB"
    ACCENT_LIGHT = "#60A5FA"
    ACCENT_GLOW = "#1D4ED8"

    SUCCESS = "#22C55E"
    SUCCESS_DIM = "#15803D"
    DANGER = "#EF4444"
    DANGER_BRIGHT = "#F87171"
    WARNING = "#F59E0B"
    INFO = "#38BDF8"

    TEXT_PRIMARY = "#F1F5F9"
    TEXT_SECONDARY = "#94A3B8"
    TEXT_MUTED = "#64748B"
    TEXT_DISABLED = "#475569"

    BORDER = "#334155"
    BORDER_LIGHT = "#475569"
    DIVIDER = "#1E293B"


class Fonts:
    """Font tuples used across CustomTkinter widgets."""

    FAMILY = "Segoe UI"

    HERO = (FAMILY, 42, "bold")
    TITLE = (FAMILY, 28, "bold")
    HEADING = (FAMILY, 22, "bold")
    SUBHEADING = (FAMILY, 16, "bold")
    BODY = (FAMILY, 14, "normal")
    BODY_BOLD = (FAMILY, 14, "bold")
    SMALL = (FAMILY, 12, "normal")
    SMALL_BOLD = (FAMILY, 12, "bold")
    TINY = (FAMILY, 10, "normal")
    BUTTON = (FAMILY, 15, "bold")
    BUTTON_SM = (FAMILY, 13, "bold")


class Spacing:
    """Spacing tokens in pixels."""

    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 20
    XXL = 28
    XXXL = 36

    CARD_PAD_X = 24
    CARD_PAD_Y = 20
    SCREEN_PAD = 30
    SECTION_GAP = 20


class Radius:
    """Border radius values."""

    SM = 6
    MD = 10
    LG = 14
    XL = 18
    PILL = 50


WINDOW_WIDTH = 850
WINDOW_HEIGHT = 650
APP_TITLE = "Instagram Red Flags"

