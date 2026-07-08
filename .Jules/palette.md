## 2024-05-18 - Clickable Rows for Toggle Switches
**Learning:** In lists with toggle switches (like the Smart Filter Dashboard), users naturally try to click the row text or empty space rather than aiming for the small switch widget itself. Making the entire row a click target significantly improves the UX by making it more forgiving and accessible.
**Action:** When implementing lists with per-row boolean toggles, bind click events to the row container and primary text labels to toggle the underlying state, and provide visual feedback by setting the cursor to a pointer (e.g., `cursor="hand2"` in Tkinter/CustomTkinter).

## 2024-05-18 - Search/Filter Empty States
**Learning:** During filtering operations (like the Smart Filter Dashboard), an empty result list without a message looks like a bug or incomplete load. Adding explicit empty states ("No users match your search.") provides necessary feedback and assures the user the app is functioning correctly.
**Action:** When implementing real-time search or filterable lists, always include a hidden-by-default empty state label that is toggled on when the number of visible rows reaches zero.

## 2026-05-06 - Hover Cursor on Buttons
**Learning:** In CustomTkinter, buttons do not automatically provide a pointer/hand cursor on hover, which reduces discoverability of interactive elements.
**Action:** When creating reusable interactive elements like `ActionButton`, explicitly set `cursor="hand2"` to provide standard visual feedback and improve UX.
## 2024-05-18 - Hover Feedback on Interactive Components
**Learning:** In CustomTkinter, interactive components like buttons do not display a pointer cursor by default on hover, which reduces discoverability of clickability and makes the interface feel less responsive.
**Action:** Always explicitly set `cursor="hand2"` on reusable interactive components (like buttons and row clicks) to provide immediate visual hover feedback.
## 2024-05-18 - Hover Feedback on Buttons
**Learning:** In CustomTkinter, buttons do not automatically change the cursor to a pointer (hand) on hover. This leads to a lack of visual feedback for interactivity, which is a standard expectation in modern UI/UX design.
**Action:** Always explicitly set `cursor="hand2"` on reusable interactive components (like `ActionButton` subclassing `ctk.CTkButton`) to ensure users receive clear visual indication that the element is clickable.
## 2026-07-08 - CustomTkinter CTkEntry Focus States
**Learning:** In CustomTkinter, `CTkEntry` widgets lack default visual focus states, which hurts keyboard accessibility as users have no visual feedback on active inputs.
**Action:** Manually bind `<FocusIn>` and `<FocusOut>` events to update visual properties like `border_color`, and bind `<Escape>` to clear text and yield focus using `focus_set()` to ensure full keyboard accessibility.
