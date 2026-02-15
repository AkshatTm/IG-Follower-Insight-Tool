"""
app.py — Main Application Class for Instagram Auditor
======================================================
Central App class that manages the window, screen transitions,
and shared state across all modules.
"""

import customtkinter as ctk
from src.theme import Colors, Fonts, WINDOW_WIDTH, WINDOW_HEIGHT, APP_TITLE


class App(ctk.CTk):
    """
    Main application window.
    Manages screen lifecycle (create → display → destroy) and shared state.
    
    Data Dictionary Keys:
    ─────────────────────
    - followers_file   : str | None   — Path to followers_1.json
    - following_file   : str | None   — Path to following.json
    - followers_set    : set[str]     — Parsed follower usernames
    - following_set    : set[str]     — Parsed following usernames
    - non_followers    : list[str]    — Users you follow who don't follow back
    - whitelist        : set[str]     — VIP usernames to keep following
    """

    def __init__(self):
        super().__init__()

        # ── Window Configuration ──────────────────────────────
        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.configure(fg_color=Colors.BG_DARKEST)

        # Center the window on screen
        self._center_window()

        # ── Shared Application Data ──────────────────────────
        # NOTE: Named 'data' (not 'state') to avoid shadowing tkinter's state() method
        self.data = {
            "followers_file": None,
            "following_file": None,
            "followers_set": set(),
            "following_set": set(),
            "non_followers": [],
            "whitelist": set(),
        }

        # ── Current Screen Tracking ──────────────────────────
        self._current_screen = None

        # ── Launch Screen 1 ──────────────────────────────────
        # Import here to avoid circular imports
        from src.screens.screen_upload import ScreenUpload
        self.switch_screen(ScreenUpload)

    def _center_window(self):
        """Position the window at the center of the display."""
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - WINDOW_WIDTH) // 2
        y = (screen_h - WINDOW_HEIGHT) // 2
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def switch_screen(self, screen_class):
        """
        Transition to a new screen.
        
        1. Destroy the current screen frame (if any)
        2. Instantiate the new screen class
        3. Pack it to fill the entire window
        
        All screen classes must accept (master, app) as constructor args,
        where `app` is this App instance (gives access to shared state).
        """
        # Tear down old screen
        if self._current_screen is not None:
            self._current_screen.destroy()
            self._current_screen = None

        # Build new screen
        new_screen = screen_class(self, self)
        new_screen.pack(fill="both", expand=True)
        self._current_screen = new_screen

    def reset_data(self):
        """Clear all data for a fresh restart (used by 'Restart' button)."""
        self.data = {
            "followers_file": None,
            "following_file": None,
            "followers_set": set(),
            "following_set": set(),
            "non_followers": [],
            "whitelist": set(),
        }
