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
    GlassCard, ActionButton
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

        # Fast, plain Python dict for storing VIP state
        self._vip_state = {
            u: (u in self.whitelist)
            for u in self.non_followers
        }

        # Lazy instantiation of Tkinter variables
        self._vip_vars = {}

        # Widget pool to avoid destroying and recreating frames
        self._row_pool = []
        self._active_rows = 0
        # Track currently filtered users
        self._filtered_users = self.non_followers.copy()

        # Pagination state
        self.PAGE_SIZE = 100
        self._visible_limit = self.PAGE_SIZE
        self._load_more_btn = None

        # Select-all toggle state
        self._all_selected = False
        # Track debounce job for search
        self._search_job = None

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

        # Empty state label
        self.empty_state_label = ctk.CTkLabel(
            self.scroll_frame,
            text="No users found matching your search.",
            font=Fonts.BODY,
            text_color=Colors.TEXT_MUTED
        )

        # Populate rows
        self._populate_rows()

    def _populate_rows(self, clear=False):
        """Create rows for the currently visible slice of filtered users with VIP toggle switches using a widget pool."""
        if clear:
            # Instead of destroying, pack_forget active rows to put them in the pool
            for pool_item in self._row_pool[:self._active_rows]:
                pool_item['row'].pack_forget()
            self._active_rows = 0

        if getattr(self, '_load_more_btn', None) is not None and self._load_more_btn.winfo_exists():
            self._load_more_btn.destroy()

        start_idx = self._active_rows
        end_idx = min(self._visible_limit, len(self._filtered_users))

        def create_toggle_handler(u, v):
            def handler(event=None):
                if event is not None:
                    new_state = not v.get()
                    v.set(new_state)
                else:
                    new_state = v.get()
                self._vip_state[u] = new_state
                self._update_counter()
            return handler

        for i in range(start_idx, end_idx):
            username = self._filtered_users[i]

            if username not in self._vip_vars:
                self._vip_vars[username] = ctk.BooleanVar(value=self._vip_state.get(username, False))
            else:
                self._vip_vars[username].set(self._vip_state.get(username, False))

            var = self._vip_vars[username]

            # Reuse or create new widget
            if self._active_rows < len(self._row_pool):
                pool_item = self._row_pool[self._active_rows]
                row = pool_item['row']
                user_label = pool_item['label']
                switch = pool_item['switch']
            else:
                row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent", height=40, cursor="hand2")
                user_label = ctk.CTkLabel(row, text="", font=Fonts.BODY, text_color=Colors.TEXT_PRIMARY, anchor="w", cursor="hand2")
                user_label.pack(side="left", fill="x", expand=True)
                switch = ctk.CTkSwitch(row, text="VIP", font=Fonts.SMALL, onvalue=True, offvalue=False, text_color=Colors.TEXT_MUTED, progress_color=Colors.SUCCESS, button_color=Colors.TEXT_SECONDARY, button_hover_color=Colors.ACCENT_LIGHT)
                switch.pack(side="right")
                self._row_pool.append({'row': row, 'label': user_label, 'switch': switch})

            user_label.configure(text=f"@{username}")
            switch.configure(variable=var)

            handler = create_toggle_handler(username, var)
            switch.configure(command=handler)

            row.bind("<Button-1>", handler)
            if hasattr(row, "_canvas"):
                row._canvas.bind("<Button-1>", handler)
            user_label.bind("<Button-1>", handler)
            if hasattr(user_label, "_label"):
                user_label._label.bind("<Button-1>", handler)

            row.pack(fill="x", padx=Spacing.MD, pady=2)
            self._active_rows += 1

        if self._visible_limit < len(self._filtered_users):
            from src.components import ActionButton
            self._load_more_btn = ActionButton(
                self.scroll_frame,
                text="Load More",
                variant="secondary",
                height=36,
                command=self._load_more
            )
            self._load_more_btn.pack(pady=(Spacing.MD, Spacing.MD))

    def _load_more(self):
        """Load the next batch of users."""
        self._visible_limit += self.PAGE_SIZE
        self._populate_rows()

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
        """Debounce the search input to avoid UI lag."""
        if self._search_job is not None:
            self.after_cancel(self._search_job)
        self._search_job = self.after(300, self._perform_search)

    def _perform_search(self):
        """Filter the visible rows based on search query using pagination."""
        query = self.search_entry.get().lower().strip()

        if query == "":
            self._filtered_users = self.non_followers.copy()
        else:
            self._filtered_users = [
                u for u in self.non_followers if query in u.lower()
            ]

        self._visible_limit = self.PAGE_SIZE
        self._populate_rows(clear=True)

        visible_count = len(self._filtered_users)

        if visible_count == 0:
            if len(self.non_followers) == 0:
                self.empty_state_label.configure(text="No non-followers to filter! 🎉")
            else:
                self.empty_state_label.configure(text="No users match your search.")
            self.empty_state_label.pack(pady=Spacing.XL)
        else:
            self.empty_state_label.pack_forget()

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
        """Toggle all VIP switches on/off for currently filtered users."""
        self._all_selected = not self._all_selected

        for username in self._filtered_users:
            # Update source of truth
            self._vip_state[username] = self._all_selected
            # Update UI if widget exists
            if username in self._vip_vars:
                self._vip_vars[username].set(self._all_selected)

        if self._all_selected:
            self.select_all_btn.configure(text="☑  Deselect All")
        else:
            self.select_all_btn.configure(text="☐  Select All")

        self._update_counter()

    def _update_counter(self):
        """Update the VIP counter display."""
        vip_count = sum(1 for state in self._vip_state.values() if state)
        total = len(self._vip_state)
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
        for username, is_vip in self._vip_state.items():
            if is_vip:
                whitelisted.add(username)

        # Save to whitelist.json
        save_whitelist(whitelisted)

        # Store in app state
        self.app.data["whitelist"] = whitelisted

        # Transition to Screen 4
        from src.screens.screen_export import ScreenExport
        self.app.switch_screen(ScreenExport)
