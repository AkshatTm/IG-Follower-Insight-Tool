# Architecture Overview

## System Summary

Instagram Red Flags is a local desktop application built with CustomTkinter and structured as a multi-screen stateful app.

## Runtime Components

| Component | File | Responsibility |
| --- | --- | --- |
| Entry point | `main.py` | Theme initialization and app startup |
| App shell | `src/app.py` | Window lifecycle, shared state, screen transitions |
| Parser | `src/parser.py` | Parse Instagram JSON formats and compute set differences |
| Whitelist persistence | `src/whitelist.py` | Load/save VIP usernames to local JSON |
| UI components | `src/components.py` | Reusable cards, labels, action buttons, popup elements |
| Theme tokens | `src/theme.py` | Design constants (colors, fonts, spacing, sizing) |
| Screens | `src/screens/*` | Flow-specific UI and behavior logic |

## Screen Flow

1. `screen_upload.py`
   - User education
   - Upload files
   - Trigger parse and analysis
2. `screen_results.py`
   - Quick stats
   - Non-follower reveal
   - TXT export or deep scan transition
3. `screen_filter.py`
   - Search/filter non-followers
   - Toggle VIP whitelist flags
   - Persist whitelist and continue
4. `screen_export.py`
   - Final filtered count
   - CSV export
   - Clipboard copy
   - App restart

## Shared State Contract

`src/app.py` maintains a shared state dictionary with these keys:

- `followers_file`: path string or null
- `following_file`: path string or null
- `followers_set`: set of usernames
- `following_set`: set of usernames
- `non_followers`: sorted list of usernames
- `whitelist`: set of VIP usernames

## Data Processing Pipeline

1. Load JSON files from local disk.
2. Extract usernames via fallback parsing patterns.
3. Build normalized sets for followers and following.
4. Compute `following - followers`.
5. Apply whitelist subtraction for final export list.

## Error Handling Strategy

- Parsing failures are surfaced to users through clear popup messaging.
- Missing or malformed whitelist files are auto-healed to empty state.
- Export failures are caught and displayed without crashing app flow.

## Local-First Privacy Model

- No network dependency for core analytics.
- No cloud upload required.
- User data remains on local machine unless manually exported by user.
