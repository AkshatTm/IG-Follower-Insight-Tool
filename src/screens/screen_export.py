"""
screen_export.py — Screen 4: Action Station (Export)
=====================================================
Final screen presenting the filtered unfollow list with export tools.

Features:
 • Final count summary (non-followers minus whitelisted VIPs)
 • Download as .CSV
 • Copy to clipboard
 • Restart (return to Screen 1)
"""

import csv
import os
from tkinter import filedialog

import customtkinter as ctk
from src.theme import Colors, Fonts, Spacing, Radius
from src.components import (
    GlassCard, GlassCardAlt, HeroStat, ActionButton,
    SubtitleLabel, ToastPopup
)


class ScreenExport(ctk.CTkFrame):
    """
    Screen 4 — Action Station.
    Shows the final filtered list and provides export options.
    """

    def __init__(self, master, app):
        super().__init__(master, fg_color=Colors.BG_DARKEST)
        self.app = app

        # Calculate final list (non-followers minus whitelisted)
        non_followers = set(app.data["non_followers"])
        whitelist = app.data.get("whitelist", set())
        self.final_list = sorted(
            list(non_followers - whitelist), key=str.lower
        )
        self.final_count = len(self.final_list)
        self.whitelist_count = len(whitelist)
        self.total_non_followers = len(non_followers)

        self._build_ui()

    # ─────────────────────────────────────
    #  UI CONSTRUCTION
    # ─────────────────────────────────────

    def _build_ui(self):
        """Assemble all UI elements for Screen 4."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=Spacing.SCREEN_PAD, pady=Spacing.SCREEN_PAD)

        # ── Header ────────────────────────────────────────
        self._build_header(container)

        # ── Hero Summary ──────────────────────────────────
        self._build_hero(container)

        # ── Stats Breakdown ───────────────────────────────
        self._build_breakdown(container)

        # ── Export Tools ──────────────────────────────────
        self._build_export_tools(container)

        # ── Navigation ────────────────────────────────────
        self._build_navigation(container)

    def _build_header(self, parent):
        """Screen title."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, Spacing.LG))

        title = ctk.CTkLabel(
            header,
            text="📊  Final Report",
            font=Fonts.TITLE,
            text_color=Colors.TEXT_PRIMARY
        )
        title.pack(anchor="center")

        subtitle = ctk.CTkLabel(
            header,
            text="Your filtered unfollow list is ready",
            font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY
        )
        subtitle.pack(anchor="center", pady=(Spacing.XS, 0))

    def _build_hero(self, parent):
        """The final count — big and prominent."""
        hero_card = GlassCard(parent)
        hero_card.pack(fill="x", pady=(0, Spacing.LG))

        hero_inner = ctk.CTkFrame(hero_card, fg_color="transparent")
        hero_inner.pack(fill="x", padx=Spacing.CARD_PAD_X, pady=Spacing.XL)

        if self.final_count > 0:
            hero = HeroStat(
                hero_inner,
                number=str(self.final_count),
                label="users to unfollow",
                number_color=Colors.DANGER_BRIGHT,
                label_color=Colors.TEXT_SECONDARY
            )
        else:
            hero = HeroStat(
                hero_inner,
                number="0",
                label="Everyone is whitelisted! Nothing to unfollow 🎉",
                number_color=Colors.SUCCESS,
                label_color=Colors.TEXT_SECONDARY
            )
        hero.pack()

    def _build_breakdown(self, parent):
        """Stats breakdown: total non-followers, whitelisted, final."""
        breakdown_frame = ctk.CTkFrame(parent, fg_color="transparent")
        breakdown_frame.pack(fill="x", pady=(0, Spacing.XL))

        breakdown_frame.columnconfigure(0, weight=1)
        breakdown_frame.columnconfigure(1, weight=1)
        breakdown_frame.columnconfigure(2, weight=1)

        stats = [
            (str(self.total_non_followers), "Total non-followers", Colors.TEXT_PRIMARY),
            (f"-{self.whitelist_count}", "Whitelisted VIPs", Colors.SUCCESS),
            (str(self.final_count), "To unfollow", Colors.DANGER_BRIGHT),
        ]

        for col, (value, desc, color) in enumerate(stats):
            card = GlassCardAlt(breakdown_frame)
            card.grid(row=0, column=col, sticky="ew",
                      padx=Spacing.XS)

            val_label = ctk.CTkLabel(
                card, text=value,
                font=Fonts.HEADING,
                text_color=color
            )
            val_label.pack(pady=(Spacing.MD, Spacing.XS))

            desc_label = ctk.CTkLabel(
                card, text=desc,
                font=Fonts.SMALL,
                text_color=Colors.TEXT_MUTED
            )
            desc_label.pack(pady=(0, Spacing.MD))

    def _build_export_tools(self, parent):
        """Export buttons: Download CSV and Copy to Clipboard."""
        export_card = GlassCard(parent)
        export_card.pack(fill="x", pady=(0, Spacing.LG))

        inner = ctk.CTkFrame(export_card, fg_color="transparent")
        inner.pack(fill="x", padx=Spacing.CARD_PAD_X, pady=Spacing.CARD_PAD_Y)

        # Title
        ctk.CTkLabel(
            inner,
            text="📥  Export Tools",
            font=Fonts.SUBHEADING,
            text_color=Colors.ACCENT_LIGHT
        ).pack(anchor="w", pady=(0, Spacing.MD))

        # Button row
        btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        btn_frame.pack(fill="x")

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        # CSV download button
        csv_btn = ActionButton(
            btn_frame,
            text="📄  Download .CSV",
            variant="primary",
            height=48,
            command=self._on_download_csv
        )
        csv_btn.grid(row=0, column=0, sticky="ew", padx=(0, Spacing.SM))

        # Clipboard copy button
        clip_btn = ActionButton(
            btn_frame,
            text="📋  Copy to Clipboard",
            variant="secondary",
            height=48,
            command=self._on_copy_clipboard
        )
        clip_btn.grid(row=0, column=1, sticky="ew", padx=(Spacing.SM, 0))

    def _build_navigation(self, parent):
        """Restart button to return to Screen 1."""
        nav_frame = ctk.CTkFrame(parent, fg_color="transparent")
        nav_frame.pack(fill="x")

        restart_btn = ActionButton(
            nav_frame,
            text="🔄  Start Over",
            variant="secondary",
            height=42,
            font=Fonts.BUTTON_SM,
            command=self._on_restart
        )
        restart_btn.pack(side="left")

        # Version/credit
        credit = ctk.CTkLabel(
            nav_frame,
            text="Instagram Auditor v1.0",
            font=Fonts.TINY,
            text_color=Colors.TEXT_MUTED
        )
        credit.pack(side="right")

    # ─────────────────────────────────────
    #  EVENT HANDLERS
    # ─────────────────────────────────────

    def _on_download_csv(self):
        """Save the final unfollow list as a .CSV file."""
        if self.final_count == 0:
            ToastPopup(
                self.app,
                title="Nothing to Export",
                message="All users are whitelisted. There's nothing to export.",
                toast_type="info",
                duration_ms=3000
            )
            return

        filepath = filedialog.asksaveasfilename(
            title="Save Unfollow List as CSV",
            defaultextension=".csv",
            initialfile="unfollow_list.csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Username", "Status"])
                    for username in self.final_list:
                        writer.writerow([username, "To Unfollow"])

                ToastPopup(
                    self.app,
                    title="CSV Exported!",
                    message=f"Saved {self.final_count} usernames to:\n{os.path.basename(filepath)}",
                    toast_type="success",
                    duration_ms=3000
                )
            except Exception as e:
                ToastPopup(
                    self.app,
                    title="Export Failed",
                    message=f"Could not save file: {str(e)[:120]}",
                    toast_type="error",
                    duration_ms=0
                )

    def _on_copy_clipboard(self):
        """Copy all usernames to the system clipboard."""
        if self.final_count == 0:
            ToastPopup(
                self.app,
                title="Nothing to Copy",
                message="All users are whitelisted. There's nothing to copy.",
                toast_type="info",
                duration_ms=3000
            )
            return

        clipboard_text = "\n".join(f"@{u}" for u in self.final_list)
        self.app.clipboard_clear()
        self.app.clipboard_append(clipboard_text)

        ToastPopup(
            self.app,
            title="Copied!",
            message=f"{self.final_count} usernames copied to your clipboard.",
            toast_type="success",
            duration_ms=2500
        )

    def _on_restart(self):
        """Clear all data and return to Screen 1."""
        self.app.reset_data()
        from src.screens.screen_upload import ScreenUpload
        self.app.switch_screen(ScreenUpload)
