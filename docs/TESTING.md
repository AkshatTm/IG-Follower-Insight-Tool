# Testing Strategy

## Goals

- Ensure parsing correctness for changing Instagram JSON formats.
- Prevent regressions in 4-screen navigation and state transitions.
- Validate persistence and export behavior across normal and edge cases.

## Current Validation Coverage

The project has validated:

- Parser correctness using sample exports in `test_data/`
- Shared-state transitions between screens
- Whitelist file creation, load, save, and malformed-file recovery
- Export logic for TXT, CSV, and clipboard behavior

## Recommended Automated Test Plan

Use `pytest` and organize tests by module:

- `tests/test_parser.py`
  - Parse list-style JSON
  - Parse wrapped dictionary-style JSON
  - Handle malformed JSON
  - Validate set difference logic
- `tests/test_whitelist.py`
  - Missing file auto-creation
  - Corrupted file fallback to empty set
  - Save and reload round-trip
- `tests/test_app_state.py`
  - State reset behavior
  - State propagation assumptions used by screens

## Manual Regression Checklist

1. Upload screen:
   - Analyze button is disabled until both files selected.
   - File labels update after selection.
2. Results screen:
   - Counts match sample data.
   - TXT export writes one username per line.
3. Filter screen:
   - Search filters rows live.
   - Select/Deselect all updates counters.
   - Whitelist persistence survives restart.
4. Export screen:
   - Final count matches `non_followers - whitelist`.
   - CSV export includes header `Username,Status`.
   - Clipboard copy uses one username per line.
   - Restart returns to screen 1 with cleared session state.

## Suggested CI Pipeline

At minimum:

1. Install dependencies
2. Run tests (`pytest -q`)
3. Run static checks (optional but recommended)
4. Block merges on failing checks