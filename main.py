"""
main.py - Entry point for Instagram Red Flags.

Run this file to launch the application:
    python main.py
"""

import customtkinter as ctk


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    from src.app import App

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

