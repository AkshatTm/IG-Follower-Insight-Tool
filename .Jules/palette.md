## 2024-05-18 - Clickable Rows for Toggle Switches
**Learning:** In lists with toggle switches (like the Smart Filter Dashboard), users naturally try to click the row text or empty space rather than aiming for the small switch widget itself. Making the entire row a click target significantly improves the UX by making it more forgiving and accessible.
**Action:** When implementing lists with per-row boolean toggles, bind click events to the row container and primary text labels to toggle the underlying state, and provide visual feedback by setting the cursor to a pointer (e.g., `cursor="hand2"` in Tkinter/CustomTkinter).

## 2024-05-18 - Search/Filter Empty States
**Learning:** During filtering operations (like the Smart Filter Dashboard), an empty result list without a message looks like a bug or incomplete load. Adding explicit empty states ("No users match your search.") provides necessary feedback and assures the user the app is functioning correctly.
**Action:** When implementing real-time search or filterable lists, always include a hidden-by-default empty state label that is toggled on when the number of visible rows reaches zero.
