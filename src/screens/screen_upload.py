"""
screen_upload.py — Screen 1: Education Dashboard
==================================================
The landing screen that educates users on how to download their
Instagram data and collects the two required JSON files.

Features:
 • Step-by-step instruction card
 • "Open Instagram Settings" browser link
 • Two file upload rows with dynamic status (green ✓ on success)
 • "Analyze Data" button (disabled until both files are loaded)
"""

import os
import webbrowser
from tkinter import filedialog

import customtkinter as ctk
from src.theme import Colors, Fonts, Spacing, Radius
from src.components import (
    GlassCard, StatusLabel, ActionButton, SubtitleLabel
)


# Instagram settings URL for data download
INSTAGRAM_DYI_URL = "https://accountscenter.instagram.com/info_and_permissions/dyi/"


class ScreenUpload(ctk.CTkFrame):
    """
    Screen 1 — Education Dashboard.
    Collects followers_1.json and following.json from the user.
    """

    def __init__(self, master, app):
        super().__init__(master, fg_color=Colors.BG_DARKEST)
        self.app = app  # Reference to main App (for shared state & screen switching)

        # Track file selection state
        self._followers_loaded = False
        self._following_loaded = False

        self._build_ui()

    # ─────────────────────────────────────
    #  UI CONSTRUCTION
    # ─────────────────────────────────────

    def _build_ui(self):
        """Assemble all UI elements for Screen 1."""

        # ── Main scrollable container ─────────────────────
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=Spacing.SCREEN_PAD, pady=Spacing.SCREEN_PAD)

        # ── Header ────────────────────────────────────────
        self._build_header(container)

        # ── Instruction Card ──────────────────────────────
        self._build_instruction_card(container)

        # ── File Upload Section ───────────────────────────
        self._build_upload_section(container)

        # ── Analyze Button ────────────────────────────────
        self._build_analyze_button(container)

    def _build_header(self, parent):
        """App title and tagline."""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, Spacing.LG))

        # Main title
        title = ctk.CTkLabel(
            header_frame,
            text="🔍  Instagram Auditor",
            font=Fonts.TITLE,
            text_color=Colors.TEXT_PRIMARY
        )
        title.pack(anchor="center")

        # Subtitle
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Find out who doesn't follow you back",
            font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY
        )
        subtitle.pack(anchor="center", pady=(Spacing.XS, 0))

    def _build_instruction_card(self, parent):
        """Step-by-step guide on how to download Instagram data."""
        card = GlassCard(parent)
        card.pack(fill="x", pady=(0, Spacing.SECTION_GAP))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=Spacing.CARD_PAD_X, pady=Spacing.CARD_PAD_Y)

        # Card title
        card_title = ctk.CTkLabel(
            inner,
            text="📋  How to get your JSON files safely:",
            font=Fonts.SUBHEADING,
            text_color=Colors.ACCENT_LIGHT
        )
        card_title.pack(anchor="w", pady=(0, Spacing.MD))

        # Steps
        steps = [
            ("1", "Go to Accounts Center → Your Information and Permissions"),
            ("2", "Click 'Download your information'"),
            ("3", "Select ONLY 'Followers and following' (to save time)"),
            ("4", "Set format to JSON, Date Range to 'All Time'"),
        ]

        for num, text in steps:
            step_frame = ctk.CTkFrame(inner, fg_color="transparent")
            step_frame.pack(fill="x", pady=Spacing.XS)

            # Step number badge
            badge = ctk.CTkLabel(
                step_frame,
                text=f"  {num}  ",
                font=Fonts.SMALL_BOLD,
                text_color=Colors.BG_DARKEST,
                fg_color=Colors.ACCENT_PRIMARY,
                corner_radius=Radius.SM,
                width=28, height=24
            )
            badge.pack(side="left", padx=(0, Spacing.MD))

            # Step text — highlight "Crucial" step 4
            text_color = Colors.WARNING if num == "4" else Colors.TEXT_SECONDARY
            font = Fonts.BODY_BOLD if num == "4" else Fonts.BODY

            step_label = ctk.CTkLabel(
                step_frame,
                text=text,
                font=font,
                text_color=text_color,
                anchor="w"
            )
            step_label.pack(side="left", fill="x", expand=True)

        # "Open Instagram Settings" button
        btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(Spacing.MD, 0))

        open_ig_btn = ActionButton(
            btn_frame,
            text="🌐  Open Instagram Settings",
            variant="secondary",
            height=38,
            font=Fonts.BUTTON_SM,
            command=lambda: webbrowser.open(INSTAGRAM_DYI_URL)
        )
        open_ig_btn.pack(side="left")

    def _build_upload_section(self, parent):
        """Two file upload rows — one for followers, one for following."""
        upload_card = GlassCard(parent)
        upload_card.pack(fill="x", pady=(0, Spacing.SECTION_GAP))

        inner = ctk.CTkFrame(upload_card, fg_color="transparent")
        inner.pack(fill="x", padx=Spacing.CARD_PAD_X, pady=Spacing.CARD_PAD_Y)

        # Section title
        section_title = ctk.CTkLabel(
            inner,
            text="📂  Upload Your Data Files",
            font=Fonts.SUBHEADING,
            text_color=Colors.ACCENT_LIGHT
        )
        section_title.pack(anchor="w", pady=(0, Spacing.MD))

        # ── Row 1: Followers ──────────────────────────────
        row1 = ctk.CTkFrame(inner, fg_color="transparent")
        row1.pack(fill="x", pady=Spacing.SM)

        self.followers_status = StatusLabel(
            row1,
            default_text="  followers_1.json not selected"
        )
        self.followers_status.pack(side="left", fill="x", expand=True)

        followers_btn = ActionButton(
            row1,
            text="Select Followers",
            variant="secondary",
            width=160, height=36,
            font=Fonts.BUTTON_SM,
            command=self._select_followers
        )
        followers_btn.pack(side="right", padx=(Spacing.MD, 0))

        # ── Row 2: Following ──────────────────────────────
        row2 = ctk.CTkFrame(inner, fg_color="transparent")
        row2.pack(fill="x", pady=Spacing.SM)

        self.following_status = StatusLabel(
            row2,
            default_text="  following.json not selected"
        )
        self.following_status.pack(side="left", fill="x", expand=True)

        following_btn = ActionButton(
            row2,
            text="Select Following",
            variant="secondary",
            width=160, height=36,
            font=Fonts.BUTTON_SM,
            command=self._select_following
        )
        following_btn.pack(side="right", padx=(Spacing.MD, 0))

    def _build_analyze_button(self, parent):
        """The main CTA — disabled until both files are loaded."""
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(Spacing.SM, 0))

        self.analyze_btn = ActionButton(
            btn_frame,
            text="⚡  Analyze Data",
            variant="primary",
            height=50,
            font=Fonts.BUTTON,
            state="disabled",
            command=self._on_analyze
        )
        self.analyze_btn.pack(fill="x")

        # Hint text
        self.hint_label = SubtitleLabel(
            btn_frame,
            text="Select both files above to begin analysis"
        )
        self.hint_label.pack(anchor="center", pady=(Spacing.SM, 0))

    # ─────────────────────────────────────
    #  EVENT HANDLERS
    # ─────────────────────────────────────

    def _select_followers(self):
        """Open file dialog for followers_1.json."""
        filepath = filedialog.askopenfilename(
            title="Select followers_1.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            # Store path in shared state
            self.app.data["followers_file"] = filepath
            self._followers_loaded = True

            # Update status label with truncated path
            display = self._truncate_path(filepath)
            self.followers_status.set_success(display)

            # Check if both files are now loaded
            self._check_ready()

    def _select_following(self):
        """Open file dialog for following.json."""
        filepath = filedialog.askopenfilename(
            title="Select following.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            # Store path in shared state
            self.app.data["following_file"] = filepath
            self._following_loaded = True

            # Update status label with truncated path
            display = self._truncate_path(filepath)
            self.following_status.set_success(display)

            # Check if both files are now loaded
            self._check_ready()

    def _check_ready(self):
        """Enable the Analyze button only when both files are selected."""
        if self._followers_loaded and self._following_loaded:
            self.analyze_btn.configure(state="normal")
            self.hint_label.configure(
                text="✓  Both files loaded — ready to analyze!",
                text_color=Colors.SUCCESS
            )
        else:
            self.analyze_btn.configure(state="disabled")

    def _on_analyze(self):
        """
        Parse both JSON files and transition to Screen 2 on success.
        On failure, show an error popup.
        """
        from src.parser import parse_instagram_json, calculate_non_followers
        from src.components import ToastPopup

        try:
            # Parse both files
            followers_set = parse_instagram_json(
                self.app.data["followers_file"]
            )
            following_set = parse_instagram_json(
                self.app.data["following_file"]
            )

            # Store in shared state
            self.app.data["followers_set"] = followers_set
            self.app.data["following_set"] = following_set
            self.app.data["non_followers"] = calculate_non_followers(
                following_set, followers_set
            )

            # Transition to Screen 2
            from src.screens.screen_results import ScreenResults
            self.app.switch_screen(ScreenResults)

        except Exception as e:
            # Show error popup
            ToastPopup(
                self.app,
                title="Parsing Error",
                message=(
                    "Invalid JSON format. Please ensure you downloaded "
                    "the correct Instagram data.\n\n"
                    f"Details: {str(e)[:120]}"
                ),
                toast_type="error",
                duration_ms=0  # Manual dismiss only
            )

    # ─────────────────────────────────────
    #  UTILITIES
    # ─────────────────────────────────────

    @staticmethod
    def _truncate_path(filepath: str, max_len: int = 45) -> str:
        """
        Truncate a file path for clean display.
        Shows: '.../<parent>/<filename>'
        """
        filename = os.path.basename(filepath)
        parent = os.path.basename(os.path.dirname(filepath))
        short = f".../{parent}/{filename}"
        if len(short) > max_len:
            return f".../{filename}"
        return short
