"""
theme.py — Centralized Design System for Instagram Auditor
===========================================================
All visual tokens (colors, fonts, spacing) are defined here.
Import this module wherever you need consistent styling.
"""


# ──────────────────────────────────────────────
#  COLOR PALETTE  (Dark mode optimized)
# ──────────────────────────────────────────────

class Colors:
    """Premium dark-mode color palette with blue accents."""

    # Backgrounds (layered for depth)
    BG_DARKEST   = "#0B0E17"     # Window background
    BG_DARK      = "#111827"     # Primary surface
    BG_CARD      = "#1A2236"     # Card / elevated surface
    BG_CARD_ALT  = "#1E293B"     # Alternate card shade
    BG_HOVER     = "#253352"     # Hover state

    # Accent — Vibrant blue gradient endpoints
    ACCENT_PRIMARY   = "#3B82F6"   # Bright blue (buttons, highlights)
    ACCENT_HOVER     = "#2563EB"   # Darker blue (hover state)
    ACCENT_LIGHT     = "#60A5FA"   # Light blue (links, subtle accents)
    ACCENT_GLOW      = "#1D4ED8"   # Deep blue glow

    # Semantic colors
    SUCCESS          = "#22C55E"   # Green — file loaded, success states
    SUCCESS_DIM      = "#15803D"   # Muted green for backgrounds
    DANGER           = "#EF4444"   # Red — traitor count, errors
    DANGER_BRIGHT    = "#F87171"   # Light red for hero numbers
    WARNING          = "#F59E0B"   # Amber — warnings
    INFO             = "#38BDF8"   # Sky blue — informational

    # Text
    TEXT_PRIMARY     = "#F1F5F9"   # Almost white — primary text
    TEXT_SECONDARY   = "#94A3B8"   # Slate gray — secondary text
    TEXT_MUTED       = "#64748B"   # Muted — placeholders, hints
    TEXT_DISABLED    = "#475569"   # Disabled state

    # Borders & dividers
    BORDER           = "#334155"   # Subtle border
    BORDER_LIGHT     = "#475569"   # Slightly visible border
    DIVIDER          = "#1E293B"   # Horizontal rules


# ──────────────────────────────────────────────
#  TYPOGRAPHY
# ──────────────────────────────────────────────

class Fonts:
    """
    Font tuples for CustomTkinter widgets.
    Format: (family, size, weight)
    We use Segoe UI on Windows (modern), fall back to Helvetica.
    """
    FAMILY = "Segoe UI"

    HERO       = (FAMILY, 42, "bold")    # Massive numbers (non-followers count)
    TITLE      = (FAMILY, 28, "bold")    # Screen titles
    HEADING    = (FAMILY, 22, "bold")    # Section headings
    SUBHEADING = (FAMILY, 16, "bold")    # Card titles, labels
    BODY       = (FAMILY, 14, "normal")  # Body text
    BODY_BOLD  = (FAMILY, 14, "bold")    # Emphasized body
    SMALL      = (FAMILY, 12, "normal")  # Captions, hints
    SMALL_BOLD = (FAMILY, 12, "bold")    # Small emphasis
    TINY       = (FAMILY, 10, "normal")  # Tooltips, fine print
    BUTTON     = (FAMILY, 15, "bold")    # Button labels
    BUTTON_SM  = (FAMILY, 13, "bold")    # Smaller buttons


# ──────────────────────────────────────────────
#  SPACING & LAYOUT
# ──────────────────────────────────────────────

class Spacing:
    """Consistent spacing tokens (in pixels)."""
    XS   = 4
    SM   = 8
    MD   = 12
    LG   = 16
    XL   = 20
    XXL  = 28
    XXXL = 36

    # Standard paddings for containers
    CARD_PAD_X  = 24
    CARD_PAD_Y  = 20
    SCREEN_PAD  = 30
    SECTION_GAP = 20


# ──────────────────────────────────────────────
#  WIDGET STYLE PRESETS
# ──────────────────────────────────────────────

class Radius:
    """Border radius values."""
    SM   = 6
    MD   = 10
    LG   = 14
    XL   = 18
    PILL = 50   # Fully rounded buttons


# Window configuration
WINDOW_WIDTH  = 850
WINDOW_HEIGHT = 650
APP_TITLE     = "Instagram Auditor"
