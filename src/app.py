"""
app.py - Main application class for Instagram Red Flags.

Central App class that manages the window, screen transitions,
and shared state across all modules.
"""

import customtkinter as ctk
from src.theme import Colors, WINDOW_WIDTH, WINDOW_HEIGHT, APP_TITLE


class App(ctk.CTk):
    """
    Main application window.
    Manages screen lifecycle (create -> display -> destroy) and shared state.

    Data dictionary keys:
    - followers_file: str | None
    - following_file: str | None
    - followers_set: set[str]
    - following_set: set[str]
    - non_followers: list[str]
    - whitelist: set[str]
    """

    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.configure(fg_color=Colors.BG_DARKEST)

        self._center_window()

        # Named 'data' (not 'state') to avoid shadowing tkinter's state() method.
        self.data = {
            "followers_file": None,
            "following_file": None,
            "followers_set": set(),
            "following_set": set(),
            "non_followers": [],
            "whitelist": set(),
        }

        self._current_screen = None

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
        """Destroy current screen and show a new screen frame."""
        if self._current_screen is not None:
            self._current_screen.destroy()
            self._current_screen = None

        new_screen = screen_class(self, self)
        new_screen.pack(fill="both", expand=True)
        self._current_screen = new_screen

    def reset_data(self):
        """Clear all data for a fresh restart."""
        self.data = {
            "followers_file": None,
            "following_file": None,
            "followers_set": set(),
            "following_set": set(),
            "non_followers": [],
            "whitelist": set(),
        }

