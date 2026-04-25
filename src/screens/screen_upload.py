"""
screen_upload.py - Screen 1: Education Dashboard.

The landing screen educates users on getting Instagram JSON files
and collects the two required files for analysis.
"""

import os
import webbrowser
from tkinter import filedialog

import customtkinter as ctk
from src.theme import Colors, Fonts, Spacing, Radius
from src.components import GlassCard, StatusLabel, ActionButton, SubtitleLabel


INSTAGRAM_DYI_URL = "https://accountscenter.instagram.com/info_and_permissions/dyi/"


class ScreenUpload(ctk.CTkFrame):
    """Screen 1 - Education dashboard and file selection."""

    def __init__(self, master, app):
        super().__init__(master, fg_color=Colors.BG_DARKEST)
        self.app = app

        self._followers_loaded = False
        self._following_loaded = False

        self._build_ui()

    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(
            fill="both",
            expand=True,
            padx=Spacing.SCREEN_PAD,
            pady=Spacing.SCREEN_PAD,
        )

        self._build_header(container)
        self._build_instruction_card(container)
        self._build_upload_section(container)
        self._build_analyze_button(container)

    def _build_header(self, parent):
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, Spacing.LG))

        title = ctk.CTkLabel(
            header_frame,
            text="Instagram Red Flags",
            font=Fonts.TITLE,
            text_color=Colors.TEXT_PRIMARY,
        )
        title.pack(anchor="center")

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Find out who does not follow you back",
            font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY,
        )
        subtitle.pack(anchor="center", pady=(Spacing.XS, 0))

    def _build_instruction_card(self, parent):
        card = GlassCard(parent)
        card.pack(fill="x", pady=(0, Spacing.SECTION_GAP))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=Spacing.CARD_PAD_X, pady=Spacing.CARD_PAD_Y)

        card_title = ctk.CTkLabel(
            inner,
            text="How to get your JSON files safely:",
            font=Fonts.SUBHEADING,
            text_color=Colors.ACCENT_LIGHT,
        )
        card_title.pack(anchor="w", pady=(0, Spacing.MD))

        steps = [
            ("1", "Go to Accounts Center -> Your Information and Permissions"),
            ("2", "Click 'Download your information'"),
            ("3", "Select ONLY 'Followers and following' (to save time)"),
            ("4", "Set format to JSON, Date Range to 'All Time'"),
        ]

        for num, text in steps:
            step_frame = ctk.CTkFrame(inner, fg_color="transparent")
            step_frame.pack(fill="x", pady=Spacing.XS)

            badge = ctk.CTkLabel(
                step_frame,
                text=f"  {num}  ",
                font=Fonts.SMALL_BOLD,
                text_color=Colors.BG_DARKEST,
                fg_color=Colors.ACCENT_PRIMARY,
                corner_radius=Radius.SM,
                width=28,
                height=24,
            )
            badge.pack(side="left", padx=(0, Spacing.MD))

            text_color = Colors.WARNING if num == "4" else Colors.TEXT_SECONDARY
            font = Fonts.BODY_BOLD if num == "4" else Fonts.BODY

            step_label = ctk.CTkLabel(
                step_frame,
                text=text,
                font=font,
                text_color=text_color,
                anchor="w",
            )
            step_label.pack(side="left", fill="x", expand=True)

        btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(Spacing.MD, 0))

        open_ig_btn = ActionButton(
            btn_frame,
            text="Open Instagram Settings",
            variant="secondary",
            height=38,
            font=Fonts.BUTTON_SM,
            command=lambda: webbrowser.open(INSTAGRAM_DYI_URL),
        )
        open_ig_btn.pack(side="left")

    def _build_upload_section(self, parent):
        upload_card = GlassCard(parent)
        upload_card.pack(fill="x", pady=(0, Spacing.SECTION_GAP))

        inner = ctk.CTkFrame(upload_card, fg_color="transparent")
        inner.pack(fill="x", padx=Spacing.CARD_PAD_X, pady=Spacing.CARD_PAD_Y)

        section_title = ctk.CTkLabel(
            inner,
            text="Upload Your Data Files",
            font=Fonts.SUBHEADING,
            text_color=Colors.ACCENT_LIGHT,
        )
        section_title.pack(anchor="w", pady=(0, Spacing.MD))

        row1 = ctk.CTkFrame(inner, fg_color="transparent")
        row1.pack(fill="x", pady=Spacing.SM)

        self.followers_status = StatusLabel(
            row1,
            default_text="  followers_1.json not selected",
        )
        self.followers_status.pack(side="left", fill="x", expand=True)

        followers_btn = ActionButton(
            row1,
            text="Select Followers",
            variant="secondary",
            width=160,
            height=36,
            font=Fonts.BUTTON_SM,
            command=self._select_followers,
        )
        followers_btn.pack(side="right", padx=(Spacing.MD, 0))

        row2 = ctk.CTkFrame(inner, fg_color="transparent")
        row2.pack(fill="x", pady=Spacing.SM)

        self.following_status = StatusLabel(
            row2,
            default_text="  following.json not selected",
        )
        self.following_status.pack(side="left", fill="x", expand=True)

        following_btn = ActionButton(
            row2,
            text="Select Following",
            variant="secondary",
            width=160,
            height=36,
            font=Fonts.BUTTON_SM,
            command=self._select_following,
        )
        following_btn.pack(side="right", padx=(Spacing.MD, 0))

    def _build_analyze_button(self, parent):
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(Spacing.SM, 0))

        self.analyze_btn = ActionButton(
            btn_frame,
            text="Analyze Data",
            variant="primary",
            height=50,
            font=Fonts.BUTTON,
            state="disabled",
            command=self._on_analyze,
        )
        self.analyze_btn.pack(fill="x")

        self.hint_label = SubtitleLabel(
            btn_frame,
            text="Select both files above to begin analysis",
        )
        self.hint_label.pack(anchor="center", pady=(Spacing.SM, 0))

    def _select_followers(self):
        filepath = filedialog.askopenfilename(
            title="Select followers_1.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if filepath:
            self.app.data["followers_file"] = filepath
            self._followers_loaded = True
            self.followers_status.set_success(self._truncate_path(filepath))
            self._check_ready()

    def _select_following(self):
        filepath = filedialog.askopenfilename(
            title="Select following.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if filepath:
            self.app.data["following_file"] = filepath
            self._following_loaded = True
            self.following_status.set_success(self._truncate_path(filepath))
            self._check_ready()

    def _check_ready(self):
        if self._followers_loaded and self._following_loaded:
            self.analyze_btn.configure(state="normal")
            self.hint_label.configure(
                text="[OK] Both files loaded - ready to analyze!",
                text_color=Colors.SUCCESS,
            )
        else:
            self.analyze_btn.configure(state="disabled")

    def _on_analyze(self):
        from src.parser import parse_instagram_json, calculate_non_followers
        from src.components import ToastPopup

        try:
            followers_set = parse_instagram_json(self.app.data["followers_file"])
            following_set = parse_instagram_json(self.app.data["following_file"])

            self.app.data["followers_set"] = followers_set
            self.app.data["following_set"] = following_set
            self.app.data["non_followers"] = calculate_non_followers(
                following_set,
                followers_set,
            )

            from src.screens.screen_results import ScreenResults

            self.app.switch_screen(ScreenResults)

        except Exception as e:
            ToastPopup(
                self.app,
                title="Parsing Error",
                message=(
                    "Invalid JSON format. Please ensure you downloaded "
                    "the correct Instagram data.\n\n"
                    f"Details: {str(e)[:120]}"
                ),
                toast_type="error",
                duration_ms=0,
            )

    @staticmethod
    def _truncate_path(filepath: str, max_len: int = 45) -> str:
        filename = os.path.basename(filepath)
        parent = os.path.basename(os.path.dirname(filepath))
        short = f".../{parent}/{filename}"
        if len(short) > max_len:
            return f".../{filename}"
        return short

