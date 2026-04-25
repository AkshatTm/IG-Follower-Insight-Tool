"""
components.py - Reusable UI components for Instagram Red Flags.
"""

import customtkinter as ctk
from src.theme import Colors, Fonts, Spacing, Radius


class GlassCard(ctk.CTkFrame):
    """A rounded card surface used to group related UI sections."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=Colors.BG_CARD,
            corner_radius=Radius.LG,
            border_width=1,
            border_color=Colors.BORDER,
            **kwargs,
        )


class GlassCardAlt(ctk.CTkFrame):
    """Alternate shade card for stat blocks and compact sections."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=Colors.BG_CARD_ALT,
            corner_radius=Radius.MD,
            border_width=1,
            border_color=Colors.BORDER,
            **kwargs,
        )


class StatusLabel(ctk.CTkLabel):
    """Label that can switch between default, success, and error states."""

    def __init__(self, master, default_text: str = "", **kwargs):
        self._default_text = default_text
        super().__init__(
            master,
            text=default_text,
            font=Fonts.BODY,
            text_color=Colors.TEXT_MUTED,
            anchor="w",
            **kwargs,
        )

    def set_success(self, text: str):
        self.configure(text=f"[OK]  {text}", text_color=Colors.SUCCESS)

    def set_error(self, text: str):
        self.configure(text=f"[X]  {text}", text_color=Colors.DANGER)

    def reset(self):
        self.configure(text=self._default_text, text_color=Colors.TEXT_MUTED)


class HeroStat(ctk.CTkFrame):
    """Large visual statistic block for key values."""

    def __init__(
        self,
        master,
        number: str = "0",
        label: str = "",
        number_color: str = Colors.DANGER_BRIGHT,
        label_color: str = Colors.TEXT_SECONDARY,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.number_label = ctk.CTkLabel(
            self,
            text=number,
            font=Fonts.HERO,
            text_color=number_color,
        )
        self.number_label.pack(pady=(Spacing.SM, Spacing.XS))

        self.desc_label = ctk.CTkLabel(
            self,
            text=label,
            font=Fonts.SUBHEADING,
            text_color=label_color,
        )
        self.desc_label.pack(pady=(0, Spacing.SM))

    def update_stat(self, number: str, label: str = None):
        self.number_label.configure(text=number)
        if label is not None:
            self.desc_label.configure(text=label)


class StatCard(ctk.CTkFrame):
    """Compact value + label card used in summary rows."""

    def __init__(
        self,
        master,
        value: str = "0",
        description: str = "",
        value_color: str = Colors.ACCENT_LIGHT,
        **kwargs,
    ):
        super().__init__(
            master,
            fg_color=Colors.BG_CARD,
            corner_radius=Radius.MD,
            border_width=1,
            border_color=Colors.BORDER,
            **kwargs,
        )

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=Fonts.HEADING,
            text_color=value_color,
        )
        self.value_label.pack(pady=(Spacing.LG, Spacing.XS))

        self.desc_label = ctk.CTkLabel(
            self,
            text=description,
            font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY,
        )
        self.desc_label.pack(pady=(0, Spacing.LG))


class ActionButton(ctk.CTkButton):
    """Styled button wrapper supporting project variants."""

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

    def __init__(
        self,
        master,
        text: str = "",
        variant: str = "primary",
        height: int = 44,
        font=None,
        **kwargs,
    ):
        style = self.VARIANTS.get(variant, self.VARIANTS["primary"]).copy()
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
            **kwargs,
        )


class SectionTitle(ctk.CTkLabel):
    """Section heading helper with consistent styling."""

    def __init__(self, master, text: str = "", **kwargs):
        super().__init__(
            master,
            text=text,
            font=Fonts.HEADING,
            text_color=Colors.TEXT_PRIMARY,
            anchor="w",
            **kwargs,
        )


class SubtitleLabel(ctk.CTkLabel):
    """Muted subtitle/helper label."""

    def __init__(self, master, text: str = "", **kwargs):
        super().__init__(
            master,
            text=text,
            font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED,
            anchor="w",
            **kwargs,
        )


class ToastPopup(ctk.CTkToplevel):
    """Temporary popup notification for info, success, warning, and error."""

    def __init__(
        self,
        master,
        title: str = "Notice",
        message: str = "",
        toast_type: str = "info",
        duration_ms: int = 3000,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.title(title)
        self.geometry("400x180")
        self.resizable(False, False)
        self.configure(fg_color=Colors.BG_DARK)

        self.attributes("-topmost", True)
        self.grab_set()

        color_map = {
            "success": Colors.SUCCESS,
            "error": Colors.DANGER,
            "info": Colors.ACCENT_LIGHT,
            "warning": Colors.WARNING,
        }
        accent = color_map.get(toast_type, Colors.ACCENT_LIGHT)

        icon_map = {
            "success": "[OK]",
            "error": "[X]",
            "info": "[i]",
            "warning": "[!]",
        }
        icon = icon_map.get(toast_type, "[i]")

        header = ctk.CTkLabel(
            self,
            text=f"{icon}  {title}",
            font=Fonts.SUBHEADING,
            text_color=accent,
        )
        header.pack(pady=(Spacing.XL, Spacing.SM))

        body = ctk.CTkLabel(
            self,
            text=message,
            font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY,
            wraplength=350,
        )
        body.pack(pady=(0, Spacing.LG))

        ok_btn = ActionButton(
            self,
            text="OK",
            variant="primary",
            width=100,
            height=36,
            command=self.destroy,
        )
        ok_btn.pack(pady=(0, Spacing.LG))

        if duration_ms > 0:
            self.after(duration_ms, self._safe_destroy)

    def _safe_destroy(self):
        try:
            self.destroy()
        except Exception:
            pass

