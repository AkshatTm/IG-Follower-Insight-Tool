"""
components.py — Reusable UI Components for Instagram Auditor
=============================================================
Premium, reusable widget building-blocks used across all screens.
"""

import customtkinter as ctk
from src.theme import Colors, Fonts, Spacing, Radius


class GlassCard(ctk.CTkFrame):
    """
    A semi-transparent elevated card with rounded corners and subtle border.
    Use this to visually group related content into distinct sections.
    """

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=Colors.BG_CARD,
            corner_radius=Radius.LG,
            border_width=1,
            border_color=Colors.BORDER,
            **kwargs
        )


class GlassCardAlt(ctk.CTkFrame):
    """Alternate shade card for visual variety (e.g., stat boxes)."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=Colors.BG_CARD_ALT,
            corner_radius=Radius.MD,
            border_width=1,
            border_color=Colors.BORDER,
            **kwargs
        )


class StatusLabel(ctk.CTkLabel):
    """
    A label that dynamically switches between default/success/error states.
    - Default: muted gray text
    - Success: green text with ✓
    - Error: red text with ✗
    """

    def __init__(self, master, default_text: str = "", **kwargs):
        self._default_text = default_text
        super().__init__(
            master,
            text=default_text,
            font=Fonts.BODY,
            text_color=Colors.TEXT_MUTED,
            anchor="w",
            **kwargs
        )

    def set_success(self, text: str):
        """Switch to green success state."""
        self.configure(
            text=f"✓  {text}",
            text_color=Colors.SUCCESS
        )

    def set_error(self, text: str):
        """Switch to red error state."""
        self.configure(
            text=f"✗  {text}",
            text_color=Colors.DANGER
        )

    def reset(self):
        """Return to default muted state."""
        self.configure(
            text=self._default_text,
            text_color=Colors.TEXT_MUTED
        )


class HeroStat(ctk.CTkFrame):
    """
    A large, visually striking statistic display.
    Shows a massive number with a descriptive label below it.
    Used for the non-followers count "hook" and export summary.
    """

    def __init__(self, master, number: str = "0", label: str = "",
                 number_color: str = Colors.DANGER_BRIGHT,
                 label_color: str = Colors.TEXT_SECONDARY, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        # The big number
        self.number_label = ctk.CTkLabel(
            self,
            text=number,
            font=Fonts.HERO,
            text_color=number_color
        )
        self.number_label.pack(pady=(Spacing.SM, Spacing.XS))

        # Descriptive text below
        self.desc_label = ctk.CTkLabel(
            self,
            text=label,
            font=Fonts.SUBHEADING,
            text_color=label_color
        )
        self.desc_label.pack(pady=(0, Spacing.SM))

    def update_stat(self, number: str, label: str = None):
        """Update the displayed number and optionally the label."""
        self.number_label.configure(text=number)
        if label is not None:
            self.desc_label.configure(text=label)


class StatCard(ctk.CTkFrame):
    """
    A compact stat card showing a value and description.
    Used in the side-by-side summary stats (following/followers count).
    """

    def __init__(self, master, value: str = "0", description: str = "",
                 value_color: str = Colors.ACCENT_LIGHT, **kwargs):
        super().__init__(
            master,
            fg_color=Colors.BG_CARD,
            corner_radius=Radius.MD,
            border_width=1,
            border_color=Colors.BORDER,
            **kwargs
        )

        # Value (large, colored)
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=Fonts.HEADING,
            text_color=value_color
        )
        self.value_label.pack(pady=(Spacing.LG, Spacing.XS))

        # Description (smaller, muted)
        self.desc_label = ctk.CTkLabel(
            self,
            text=description,
            font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY
        )
        self.desc_label.pack(pady=(0, Spacing.LG))


class ActionButton(ctk.CTkButton):
    """
    A premium styled button with hover animation.
    Supports 'primary', 'secondary', and 'danger' variants.
    """

    VARIANTS = {
        "primary": {
            "fg_color": Colors.ACCENT_PRIMARY,
            "hover_color": Colors.ACCENT_HOVER,
            "text_color": Colors.TEXT_PRIMARY,
        },
        "secondary": {
            "fg_color": Colors.BG_CARD,
            "hover_color": Colors.BG_HOVER,
            "text_color": Colors.TEXT_PRIMARY,
            "border_width": 1,
            "border_color": Colors.BORDER_LIGHT,
        },
        "danger": {
            "fg_color": Colors.DANGER,
            "hover_color": "#DC2626",
            "text_color": Colors.TEXT_PRIMARY,
        },
        "success": {
            "fg_color": Colors.SUCCESS,
            "hover_color": Colors.SUCCESS_DIM,
            "text_color": Colors.TEXT_PRIMARY,
        },
    }

    def __init__(self, master, text: str = "", variant: str = "primary",
                 height: int = 44, font=None, **kwargs):
        style = self.VARIANTS.get(variant, self.VARIANTS["primary"]).copy()
        # Allow kwargs to override variant defaults
        for key in list(style.keys()):
            if key in kwargs:
                style.pop(key)

        super().__init__(
            master,
            text=text,
            font=font or Fonts.BUTTON,
            height=height,
            corner_radius=Radius.MD,
            **style,
            **kwargs
        )


class SectionTitle(ctk.CTkLabel):
    """A styled section heading with consistent formatting."""

    def __init__(self, master, text: str = "", **kwargs):
        super().__init__(
            master,
            text=text,
            font=Fonts.HEADING,
            text_color=Colors.TEXT_PRIMARY,
            anchor="w",
            **kwargs
        )


class SubtitleLabel(ctk.CTkLabel):
    """A muted subtitle / helper text label."""

    def __init__(self, master, text: str = "", **kwargs):
        super().__init__(
            master,
            text=text,
            font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED,
            anchor="w",
            **kwargs
        )


class ToastPopup(ctk.CTkToplevel):
    """
    A temporary popup notification (success/error/info).
    Auto-closes after a set duration, or can be dismissed manually.
    """

    def __init__(self, master, title: str = "Notice",
                 message: str = "", toast_type: str = "info",
                 duration_ms: int = 3000, **kwargs):
        super().__init__(master, **kwargs)

        # Window setup
        self.title(title)
        self.geometry("400x180")
        self.resizable(False, False)
        self.configure(fg_color=Colors.BG_DARK)

        # Bring to front
        self.attributes("-topmost", True)
        self.grab_set()

        # Color based on type
        color_map = {
            "success": Colors.SUCCESS,
            "error": Colors.DANGER,
            "info": Colors.ACCENT_LIGHT,
            "warning": Colors.WARNING,
        }
        accent = color_map.get(toast_type, Colors.ACCENT_LIGHT)

        # Icon + Title
        icon_map = {"success": "✓", "error": "✗", "info": "ℹ", "warning": "⚠"}
        icon = icon_map.get(toast_type, "ℹ")

        header = ctk.CTkLabel(
            self,
            text=f"{icon}  {title}",
            font=Fonts.SUBHEADING,
            text_color=accent
        )
        header.pack(pady=(Spacing.XL, Spacing.SM))

        # Message body
        body = ctk.CTkLabel(
            self,
            text=message,
            font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=350
        )
        body.pack(pady=(0, Spacing.LG))

        # OK button
        ok_btn = ActionButton(
            self, text="OK", variant="primary",
            width=100, height=36,
            command=self.destroy
        )
        ok_btn.pack(pady=(0, Spacing.LG))

        # Auto-close after duration (0 = manual only)
        if duration_ms > 0:
            self.after(duration_ms, self._safe_destroy)

    def _safe_destroy(self):
        """Destroy only if still alive."""
        try:
            self.destroy()
        except Exception:
            pass
