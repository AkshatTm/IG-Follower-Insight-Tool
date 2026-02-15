"""
screen_filter.py — Screen 3: Smart Filter Dashboard
=====================================================
Allows users to review non-followers and whitelist VIP accounts
(influencers, celebrities) they want to keep following.

Features:
 • Real-time search filtering
 • VIP toggle switches per user
 • Persistent whitelist (whitelist.json)
 • Select All / Deselect All toggle
 • Dynamic counter showing VIP count
"""

import customtkinter as ctk
from src.theme import Colors, Fonts, Spacing, Radius
from src.components import (
    GlassCard, ActionButton, SubtitleLabel, ToastPopup
)
from src.whitelist import load_whitelist, save_whitelist


class ScreenFilter(ctk.CTkFrame):
    """
    Screen 3 — Smart Filter Dashboard.
    Review non-followers and mark VIPs to exclude from the unfollow list.
    """

    def __init__(self, master, app):
        super().__init__(master, fg_color=Colors.BG_DARKEST)
        self.app = app

        # Data
        self.non_followers = list(app.data["non_followers"])  # Mutable copy
        self.whitelist = load_whitelist()

        # Track VIP switches: {username: BooleanVar}
        self._vip_vars = {}
        # Track row widgets for search filtering: {username: frame_widget}
        self._row_widgets = {}
        # Select-all toggle state
        self._all_selected = False

        self._build_ui()

    # ─────────────────────────────────────
    #  UI CONSTRUCTION
    # ─────────────────────────────────────

    def _build_ui(self):
        """Assemble all UI elements for Screen 3."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=Spacing.SCREEN_PAD, pady=Spacing.SCREEN_PAD)

        # ── Header ────────────────────────────────────────
        self._build_header(container)

        # ── Search Bar ────────────────────────────────────
        self._build_search(container)

        # ── Scrollable User List ──────────────────────────
        self._build_user_list(container)

        # ── Footer Action Bar ─────────────────────────────
        self._build_footer(container)

    def _build_header(self, parent):
        """Screen title with dynamic subtitle."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, Spacing.LG))

        title = ctk.CTkLabel(
            header,
            text="🎯  Filter Your List",
            font=Fonts.TITLE,
            text_color=Colors.TEXT_PRIMARY
        )
        title.pack(anchor="center")

        self.subtitle = ctk.CTkLabel(
            header,
            text=f"Showing {len(self.non_followers)} users who don't follow you back",
            font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY
        )
        self.subtitle.pack(anchor="center", pady=(Spacing.XS, 0))

    def _build_search(self, parent):
        """Real-time search bar to filter the user list."""
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, Spacing.MD))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍  Search by username...",
            font=Fonts.BODY,
            height=40,
            corner_radius=Radius.MD,
            fg_color=Colors.BG_CARD,
            border_color=Colors.BORDER,
            text_color=Colors.TEXT_PRIMARY,
            placeholder_text_color=Colors.TEXT_MUTED
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", self._on_search)

    def _build_user_list(self, parent):
        """Scrollable frame populated with username rows + VIP switches."""
        # Container card
        list_card = GlassCard(parent)
        list_card.pack(fill="both", expand=True, pady=(0, Spacing.MD))

        # Column headers
        header_frame = ctk.CTkFrame(list_card, fg_color="transparent")
        header_frame.pack(fill="x", padx=Spacing.CARD_PAD_X, pady=(Spacing.MD, Spacing.XS))

        ctk.CTkLabel(
            header_frame,
            text="USERNAME",
            font=Fonts.SMALL_BOLD,
            text_color=Colors.TEXT_MUTED
        ).pack(side="left")

        ctk.CTkLabel(
            header_frame,
            text="WHITELIST",
            font=Fonts.SMALL_BOLD,
            text_color=Colors.TEXT_MUTED
        ).pack(side="right")

        # Divider
        divider = ctk.CTkFrame(list_card, fg_color=Colors.BORDER, height=1)
        divider.pack(fill="x", padx=Spacing.CARD_PAD_X)

        # Scrollable list
        self.scroll_frame = ctk.CTkScrollableFrame(
            list_card,
            fg_color="transparent",
            scrollbar_button_color=Colors.BG_HOVER,
            scrollbar_button_hover_color=Colors.ACCENT_PRIMARY
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=Spacing.SM, pady=Spacing.SM)

        # Populate rows
        self._populate_rows()

    def _populate_rows(self):
        """Create a row for each non-follower with a VIP toggle switch."""
        for username in self.non_followers:
            # Create a BooleanVar for this user's VIP state
            var = ctk.BooleanVar(
                value=(username in self.whitelist)
            )
            self._vip_vars[username] = var

            # Row frame
            row = ctk.CTkFrame(
                self.scroll_frame,
                fg_color="transparent",
                height=40
            )
            row.pack(fill="x", padx=Spacing.MD, pady=2)

            # Username label
            user_label = ctk.CTkLabel(
                row,
                text=f"@{username}",
                font=Fonts.BODY,
                text_color=Colors.TEXT_PRIMARY,
                anchor="w"
            )
            user_label.pack(side="left", fill="x", expand=True)

            # VIP switch
            switch = ctk.CTkSwitch(
                row,
                text="VIP",
                font=Fonts.SMALL,
                variable=var,
                onvalue=True,
                offvalue=False,
                text_color=Colors.TEXT_MUTED,
                progress_color=Colors.SUCCESS,
                button_color=Colors.TEXT_SECONDARY,
                button_hover_color=Colors.ACCENT_LIGHT,
                command=self._update_counter
            )
            switch.pack(side="right")

            # Store reference for search filtering
            self._row_widgets[username] = row

    def _build_footer(self, parent):
        """Footer with Select All toggle, counter, and Next button."""
        footer = ctk.CTkFrame(parent, fg_color="transparent")
        footer.pack(fill="x")

        # Left side: Select All + Counter
        left = ctk.CTkFrame(footer, fg_color="transparent")
        left.pack(side="left")

        self.select_all_btn = ActionButton(
            left,
            text="☐  Select All",
            variant="secondary",
            width=140, height=40,
            font=Fonts.BUTTON_SM,
            command=self._toggle_select_all
        )
        self.select_all_btn.pack(side="left", padx=(0, Spacing.MD))

        self.counter_label = ctk.CTkLabel(
            left,
            text="",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED
        )
        self.counter_label.pack(side="left")
        self._update_counter()

        # Right side: Next button
        next_btn = ActionButton(
            footer,
            text="Next: Review & Export  →",
            variant="primary",
            width=220, height=44,
            command=self._on_next
        )
        next_btn.pack(side="right")

    # ─────────────────────────────────────
    #  EVENT HANDLERS
    # ─────────────────────────────────────

    def _on_search(self, event=None):
        """Filter the visible rows based on search query."""
        query = self.search_entry.get().lower().strip()

        visible_count = 0
        for username, row_widget in self._row_widgets.items():
            if query == "" or query in username.lower():
                row_widget.pack(fill="x", padx=Spacing.MD, pady=2)
                visible_count += 1
            else:
                row_widget.pack_forget()

        # Update subtitle with filtered count
        if query:
            self.subtitle.configure(
                text=f"Showing {visible_count} of {len(self.non_followers)} users (filtered)"
            )
        else:
            self.subtitle.configure(
                text=f"Showing {len(self.non_followers)} users who don't follow you back"
            )

    def _toggle_select_all(self):
        """Toggle all VIP switches on/off."""
        self._all_selected = not self._all_selected

        for var in self._vip_vars.values():
            var.set(self._all_selected)

        if self._all_selected:
            self.select_all_btn.configure(text="☑  Deselect All")
        else:
            self.select_all_btn.configure(text="☐  Select All")

        self._update_counter()

    def _update_counter(self):
        """Update the VIP counter display."""
        vip_count = sum(1 for var in self._vip_vars.values() if var.get())
        total = len(self._vip_vars)
        to_unfollow = total - vip_count

        self.counter_label.configure(
            text=f"  {vip_count} whitelisted  ·  {to_unfollow} to unfollow"
        )

    def _on_next(self):
        """
        Save the whitelist and transition to Screen 4 (Export).
        """
        # Collect whitelisted usernames
        whitelisted = set()
        for username, var in self._vip_vars.items():
            if var.get():
                whitelisted.add(username)

        # Save to whitelist.json
        save_whitelist(whitelisted)

        # Store in app state
        self.app.data["whitelist"] = whitelisted

        # Transition to Screen 4
        from src.screens.screen_export import ScreenExport
        self.app.switch_screen(ScreenExport)
