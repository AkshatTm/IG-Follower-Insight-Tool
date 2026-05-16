## 2024-04-25 - Tkinter Search Debouncing and Layout Optimization
**Learning:** Calling `pack()` or `pack_forget()` on thousands of Tkinter widgets during rapid keystrokes completely blocks the main thread. Furthermore, calling `pack()` on an already packed widget, or `pack_forget()` on an already hidden widget, triggers unnecessary layout recalculations.
**Action:** Always debounce text input events that trigger layout changes (`after()` method). Additionally, check `winfo_ismapped()` before applying layout changes to avoid redundant Tkinter operations.
## 2024-04-25 - Tkinter Layout State Checks
**Learning:** `winfo_ismapped()` checks if a widget is currently visible/drawn on screen, NOT if it is managed by the layout manager. Using it to optimize `pack()` or `pack_forget()` calls leads to bugs (e.g., if the window is minimized or hidden when the check runs). Furthermore, calling `pack_forget()` on an already hidden widget is virtually a no-op in Tkinter, making manual state checks unnecessary.
**Action:** Do not use `winfo_ismapped()` to guard layout manager calls. Rely on debouncing to prevent excessive layout thrashing, and let Tkinter handle redundant `pack_forget()` operations safely.
## 2024-05-24 - [Pagination for Large UI Lists in CustomTkinter]
**Learning:** CustomTkinter completely freezes the main UI thread when instantiating thousands of widgets (e.g. 5000 rows in a CTkScrollableFrame took 10+ seconds). Furthermore, packing and repacking these widgets during search causes severe lag.
**Action:** Always implement pagination (e.g. rendering 100 items with a "Load More" button) rather than rendering full lists simultaneously. To preserve state across pagination and filtering resets, initialize the underlying item state for *all* items upfront in plain Python data structures. **Superseded clarification (see 2024-05-28): do not pre-initialize `ctk.BooleanVar` or other Tk variable wrappers for every item.**

## 2024-05-28 - Lazy Initialization of Tkinter Variables
**Learning:** Eagerly instantiating thousands of variable wrappers (like `ctk.BooleanVar`) blocks the main thread in CustomTkinter/Tkinter applications. This was causing a severe bottleneck during the initialization of the list view for Instagram exports.
**Action:** This is the current recommendation: store core state in plain Python dictionaries for all items, and lazily instantiate Tk variables only when their corresponding UI widgets are explicitly rendered on screen (e.g. via pagination or virtualization).
## 2024-05-29 - Pre-compile Regex
**Learning:** Re-compiling regular expressions inside high-volume loops (like processing thousands of usernames in an Instagram export) causes unnecessary parsing and lookup overhead.
**Action:** Explicitly pre-compile the regex at the module level using `re.compile()` to reduce overhead in high-volume operations.
