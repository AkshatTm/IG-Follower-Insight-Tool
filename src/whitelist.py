"""
whitelist.py — Whitelist Persistence Module
=============================================
Handles saving/loading the VIP whitelist to/from a local JSON file.
Users who are whitelisted are "safe" influencers/celebrities that
the user wants to keep following even if they don't follow back.
"""

import json
import os
from typing import Set

# Default whitelist file location (same directory as the app)
WHITELIST_FILE = "whitelist.json"


def _write_empty_whitelist(filepath: str):
    """Create/reset an empty whitelist file without raising UI-breaking errors."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)
    except OSError:
        # Non-fatal: app can still continue with in-memory whitelist state.
        pass


def load_whitelist(filepath: str = WHITELIST_FILE) -> Set[str]:
    """
    Load the whitelist from a JSON file.
    
    Returns an empty set if the file doesn't exist yet
    (first-time run scenario).
    
    Args:
        filepath: Path to the whitelist JSON file.
    
    Returns:
        Set of whitelisted usernames.
    """
    if not os.path.exists(filepath):
        _write_empty_whitelist(filepath)
        return set()

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                cleaned = {
                    str(username).strip()
                    for username in data
                    if isinstance(username, str) and str(username).strip()
                }
                return cleaned
            _write_empty_whitelist(filepath)
            return set()
    except (json.JSONDecodeError, IOError):
        # Corrupted file — start fresh
        _write_empty_whitelist(filepath)
        return set()


def save_whitelist(usernames: Set[str], filepath: str = WHITELIST_FILE):
    """
    Save the whitelist to a JSON file.
    
    Args:
        usernames: Set of whitelisted usernames.
        filepath: Path to write the whitelist JSON file.
    """
    sorted_list = sorted(list(usernames), key=str.lower)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(sorted_list, f, indent=2, ensure_ascii=False)
