"""
screen_results.py — Screen 2: Quick Analysis Results
======================================================
Displays the parsed results after JSON analysis:
 • Summary stats (following count, followers count)
 • Hero statistic (non-followers count, big and red)
 • Action buttons: Export List & Exit, Deep Scan

This is the "hook" screen — the dramatic reveal of how many
people don't follow the user back.
"""

import os
from tkinter import filedialog

import customtkinter as ctk
from src.theme import Colors, Fonts, Spacing, Radius
from src.components import (
    GlassCard, HeroStat, StatCard, ActionButton,
    SubtitleLabel, ToastPopup
)


class ScreenResults(ctk.CTkFrame):
    """
    Screen 2 — Quick Analysis Results.
    Shows follower stats and the non-followers count.
    """

    def __init__(self, master, app):
        super().__init__(master, fg_color=Colors.BG_DARKEST)
        self.app = app

        # Pull data from shared state
        self.following_count = len(app.data["following_set"])
        self.followers_count = len(app.data["followers_set"])
        self.non_followers = app.data["non_followers"]
        self.non_followers_count = len(self.non_followers)

        self._build_ui()

    # ─────────────────────────────────────
    #  UI CONSTRUCTION
    # ─────────────────────────────────────

    def _build_ui(self):
        """Assemble all UI elements for Screen 2."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=Spacing.SCREEN_PAD, pady=Spacing.SCREEN_PAD)

        # ── Header ────────────────────────────────────────
        self._build_header(container)

        # ── Summary Stats ─────────────────────────────────
        self._build_stats(container)

        # ── Hero Stat (The Hook) ──────────────────────────
        self._build_hero(container)

        # ── Action Buttons ────────────────────────────────
        self._build_actions(container)

    def _build_header(self, parent):
        """Screen title and success badge."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, Spacing.XL))

        # Success indicator
        badge_frame = ctk.CTkFrame(header, fg_color="transparent")
        badge_frame.pack(anchor="center")

        success_dot = ctk.CTkLabel(
            badge_frame,
            text="  ✓  Analysis Complete  ",
            font=Fonts.SMALL_BOLD,
            text_color=Colors.SUCCESS,
            fg_color=Colors.SUCCESS_DIM,
            corner_radius=Radius.PILL
        )
        success_dot.pack(pady=(0, Spacing.MD))

        title = ctk.CTkLabel(
            header,
            text="Quick Analysis Complete",
            font=Fonts.TITLE,
            text_color=Colors.TEXT_PRIMARY
        )
        title.pack(anchor="center")

    def _build_stats(self, parent):
        """Side-by-side stat cards: following count and followers count."""
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, Spacing.LG))

        # Configure grid for two equal columns
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)

        # Following card
        following_card = StatCard(
            stats_frame,
            value=str(self.following_count),
            description="accounts you follow",
            value_color=Colors.ACCENT_LIGHT
        )
        following_card.grid(row=0, column=0, sticky="ew", padx=(0, Spacing.SM))

        # Followers card
        followers_card = StatCard(
            stats_frame,
            value=str(self.followers_count),
            description="accounts following you",
            value_color=Colors.ACCENT_LIGHT
        )
        followers_card.grid(row=0, column=1, sticky="ew", padx=(Spacing.SM, 0))

    def _build_hero(self, parent):
        """The dramatic non-followers count — big, red, attention-grabbing."""
        hero_card = GlassCard(parent)
        hero_card.pack(fill="x", pady=(0, Spacing.XL))

        hero_inner = ctk.CTkFrame(hero_card, fg_color="transparent")
        hero_inner.pack(fill="x", padx=Spacing.CARD_PAD_X, pady=Spacing.XXL)

        # Preamble text
        found_label = ctk.CTkLabel(
            hero_inner,
            text="Found",
            font=Fonts.SUBHEADING,
            text_color=Colors.TEXT_SECONDARY
        )
        found_label.pack()

        # THE BIG NUMBER
        hero_stat = HeroStat(
            hero_inner,
            number=str(self.non_followers_count),
            label="people who don't follow you back",
            number_color=Colors.DANGER_BRIGHT,
            label_color=Colors.TEXT_SECONDARY
        )
        hero_stat.pack(pady=(0, Spacing.XS))

        # Contextual hint
        if self.non_followers_count > 0:
            pct = round(
                (self.non_followers_count / max(self.following_count, 1)) * 100
            )
            hint_text = f"That's ~{pct}% of the people you follow"
        else:
            hint_text = "Everyone you follow also follows you back! 🎉"

        hint = ctk.CTkLabel(
            hero_inner,
            text=hint_text,
            font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED
        )
        hint.pack()

    def _build_actions(self, parent):
        """Two action buttons: Export & Exit, Deep Scan."""
        actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        actions_frame.pack(fill="x", side="bottom")

        # Configure grid for two equal columns
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)

        # ── Button 1: Export List & Exit ──────────────────
        export_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        export_frame.grid(row=0, column=0, sticky="ew", padx=(0, Spacing.SM))

        export_btn = ActionButton(
            export_frame,
            text="📄  Export List & Exit",
            variant="secondary",
            height=54,
            command=self._on_export
        )
        export_btn.pack(fill="x")

        export_hint = SubtitleLabel(
            export_frame,
            text="Save non-followers as .txt file"
        )
        export_hint.pack(anchor="center", pady=(Spacing.XS, 0))

        # ── Button 2: Deep Scan ───────────────────────────
        deep_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        deep_frame.grid(row=0, column=1, sticky="ew", padx=(Spacing.SM, 0))

        deep_btn = ActionButton(
            deep_frame,
            text="🔬  Deep Scan (Identify Influencers)",
            variant="primary",
            height=54,
            command=self._on_deep_scan
        )
        deep_btn.pack(fill="x")

        deep_hint = SubtitleLabel(
            deep_frame,
            text="Requires a burner account to filter verified/famous accounts"
        )
        deep_hint.pack(anchor="center", pady=(Spacing.XS, 0))

    # ─────────────────────────────────────
    #  EVENT HANDLERS
    # ─────────────────────────────────────

    def _on_export(self):
        """Save the non-followers list to a .txt file, then quit."""
        filepath = filedialog.asksaveasfilename(
            title="Save Non-Followers List",
            defaultextension=".txt",
            initialfile="traitors.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    for username in self.non_followers:
                        f.write(f"{username}\n")

                # Success popup, then quit
                ToastPopup(
                    self.app,
                    title="Exported Successfully!",
                    message=f"Saved {self.non_followers_count} usernames to:\n{os.path.basename(filepath)}",
                    toast_type="success",
                    duration_ms=2500
                )
                # Quit after popup closes
                self.app.after(3000, self.app.quit)

            except Exception as e:
                ToastPopup(
                    self.app,
                    title="Export Failed",
                    message=f"Could not save file: {str(e)[:120]}",
                    toast_type="error",
                    duration_ms=0
                )

    def _on_deep_scan(self):
        """
        Transition to Module 2 — Screen 3 (Smart Filter).
        This is where the user can whitelist VIPs/influencers.
        """
        print("Transitioning to Module 2...")
        from src.screens.screen_filter import ScreenFilter
        self.app.switch_screen(ScreenFilter)
