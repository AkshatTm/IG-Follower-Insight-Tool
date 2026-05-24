"""
parser.py — Instagram JSON Data Parser
========================================
Robustly parses Instagram's data export JSON files
and calculates the set difference (non-followers).

Instagram's JSON structure changes frequently, so we
try multiple known patterns to extract usernames.
"""

import json
import os
import re
from typing import Set, List

# Pre-compile the regex used for username cleanup to avoid compilation overhead inside large iteration loops.
USERNAME_CLEANUP_REGEX = re.compile(r'[^a-zA-Z0-9._]')


def parse_instagram_json(filepath: str) -> Set[str]:
    """
    Parse an Instagram JSON data export file and extract usernames.
    
    Instagram has used multiple JSON structures over time:
      Pattern A (current):  [ { "string_list_data": [{"value": "username"}] } ]
      Pattern B (wrapped):  { "relationships_...": [ { "string_list_data": [...] } ] }
      Pattern C (flat):     [ { "value": "username" } ]
    
    Args:
        filepath: Path to the JSON file (followers_1.json or following.json)
    
    Returns:
        A set of unique username strings.
    
    Raises:
        ValueError: If the JSON structure is unrecognized.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    # Security: Prevent Memory Exhaustion (DoS)
    # Check if the path is a regular file. Character devices like /dev/zero
    # return a size of 0 but can produce infinite data, leading to memory exhaustion.
    if not os.path.isfile(filepath):
        raise ValueError(
            f"Invalid file path '{filepath}'. "
            "Only regular files are allowed to prevent DoS attacks."
        )

    # Limit to 100MB before parsing — very large JSON files can crash the app.
    max_size_bytes = 100 * 1024 * 1024
    if os.path.getsize(filepath) > max_size_bytes:
        raise ValueError(
            "File too large. Maximum allowed size is 100MB to "
            "prevent memory exhaustion."
        )

    # Instagram exports files in latin-1 (ISO-8859-1), not UTF-8.
    # Try UTF-8 first (covers newer exports), then fall back to latin-1.
    raw_text = None
    for encoding in ("utf-8", "latin-1", "utf-8-sig"):
        try:
            with open(filepath, "r", encoding=encoding) as f:
                raw_text = f.read()
            break
        except UnicodeDecodeError:
            continue

    if raw_text is None:
        raise ValueError(
            f"Could not decode '{os.path.basename(filepath)}'. "
            "The file encoding is not supported."
        )

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise json.JSONDecodeError(
            f"'{os.path.basename(filepath)}' is not valid JSON: {exc.msg}",
            exc.doc,
            exc.pos,
        ) from exc

    usernames = set()

    # ── Pattern B: Data wrapped in a top-level key ────────
    # e.g. { "relationships_following": [ ... ] }
    if isinstance(data, dict):
        # Find the first key that contains a list
        for key, value in data.items():
            if isinstance(value, list):
                data = value
                break
        else:
            raise ValueError(
                f"Unrecognized JSON structure in '{filepath}'. "
                "Expected a list or a dict containing a list."
            )

    # ── Pattern A / C: Data is a list ─────────────────────
    if isinstance(data, list):
        for entry in data:
            username = _extract_username(entry)
            if username:
                usernames.add(username)
    else:
        raise ValueError(
            f"Unrecognized JSON structure in '{filepath}'. "
            "Top-level data must be a list."
        )

    if not usernames:
        raise ValueError(
            f"No usernames found in '{os.path.basename(filepath)}'. "
            "The file might be empty or have an unexpected format. "
            "Make sure you selected the correct Instagram export files."
        )

    return usernames


def _extract_username(entry: dict) -> str | None:
    """
    Extract a username from a single entry using multiple patterns.
    
    Tries (in order):
      1. entry['string_list_data'][0]['value']   — Most common pattern
      2. entry['title']                           — Newer Instagram export (following.json)
      3. entry['value']                           — Flat pattern
      4. entry['username']                        — Direct pattern
    
    Returns the username string or None if extraction fails.
    """
    if not isinstance(entry, dict):
        return None

    # Security: Limit username length to 100 characters to prevent artificially
    # massive strings from freezing the UI when rendered (DoS mitigation).
    max_len = 100

    # Pattern A: string_list_data array (most common Instagram format)
    try:
        sld = entry.get("string_list_data", [])
        if isinstance(sld, list) and len(sld) > 0:
            value = sld[0].get("value", "")
            if isinstance(value, str) and value.strip():
                # [SECURITY]: Sanitize username to prevent downstream format injection (CSV/Formula injection)
                clean_value = USERNAME_CLEANUP_REGEX.sub('', value.strip()[:max_len])
                if clean_value:
                    return clean_value
    except (AttributeError, IndexError, TypeError):
        pass

    # Pattern E: Top-level "title" key — newer Instagram following.json exports
    # store the username in entry["title"] when string_list_data has no "value".
    try:
        value = entry.get("title", "")
        if isinstance(value, str) and value.strip():
            # [SECURITY]: Sanitize username to prevent downstream format injection (CSV/Formula injection)
            clean_value = USERNAME_CLEANUP_REGEX.sub('', value.strip()[:max_len])
            if clean_value:
                return clean_value
    except (AttributeError, TypeError):
        pass

    # Pattern C: Flat {"value": "username"}
    try:
        value = entry.get("value", "")
        if isinstance(value, str) and value.strip():
            # [SECURITY]: Sanitize username to prevent downstream format injection (CSV/Formula injection)
            clean_value = USERNAME_CLEANUP_REGEX.sub('', value.strip()[:max_len])
            if clean_value:
                return clean_value
    except (AttributeError, TypeError):
        pass

    # Pattern D: Direct {"username": "username"}
    try:
        value = entry.get("username", "")
        if isinstance(value, str) and value.strip():
            # [SECURITY]: Sanitize username to prevent downstream format injection (CSV/Formula injection)
            clean_value = USERNAME_CLEANUP_REGEX.sub('', value.strip()[:max_len])
            if clean_value:
                return clean_value
    except (AttributeError, TypeError):
        pass

    return None


def calculate_non_followers(following_set: Set[str],
                             followers_set: Set[str]) -> List[str]:
    """
    Calculate users you follow who don't follow you back.
    
    Args:
        following_set: People you are following
        followers_set: People who follow you
    
    Returns:
        Sorted list of usernames (following - followers).
    """
    non_followers = following_set - followers_set
    return sorted(list(non_followers), key=str.lower)
