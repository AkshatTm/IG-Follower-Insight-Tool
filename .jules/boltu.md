## 2024-04-25 - Tkinter Search Debouncing and Layout Optimization
**Learning:** Calling `pack()` or `pack_forget()` on thousands of Tkinter widgets during rapid keystrokes completely blocks the main thread. Furthermore, calling `pack()` on an already packed widget, or `pack_forget()` on an already hidden widget, triggers unnecessary layout recalculations.
**Action:** Always debounce text input events that trigger layout changes (`after()` method). Additionally, check `winfo_ismapped()` before applying layout changes to avoid redundant Tkinter operations.
## 2024-04-25 - Tkinter Layout State Checks
**Learning:** `winfo_ismapped()` checks if a widget is currently visible/drawn on screen, NOT if it is managed by the layout manager. Using it to optimize `pack()` or `pack_forget()` calls leads to bugs (e.g., if the window is minimized or hidden when the check runs). Furthermore, calling `pack_forget()` on an already hidden widget is virtually a no-op in Tkinter, making manual state checks unnecessary.
**Action:** Do not use `winfo_ismapped()` to guard layout manager calls. Rely on debouncing to prevent excessive layout thrashing, and let Tkinter handle redundant `pack_forget()` operations safely.
## 2024-05-24 - [Pagination for Large UI Lists in CustomTkinter]
**Learning:** CustomTkinter completely freezes the main UI thread when instantiating thousands of widgets (e.g. 5000 rows in a CTkScrollableFrame took 10+ seconds). Furthermore, packing and repacking these widgets during search causes severe lag.
**Action:** Always implement pagination (e.g. rendering 100 items with a "Load More" button) rather than rendering full lists simultaneously.
## 2026-04-30 - JSON Parsing Dictionary Overhead
**Learning:** Using `try/except` blocks and `.get()` for dictionary key lookups when parsing heterogeneous JSON lists where keys are frequently missing adds significant execution overhead.
**Action:** Use direct key existence checks (e.g., `if 'key' in dict:`) instead to significantly improve parsing speed for large JSON arrays.
## 2026-04-30 - Lazy Initialization of Tkinter Variables
**Learning:** Pre-initializing thousands of `ctk.BooleanVar` or `tk.Variable` instances upfront (e.g., for state tracking of 500k rows) severely blocks the main UI thread, taking up to several seconds just to instantiate. This causes massive perceived app lag when a screen loads.
**Action:** Always map application state to simple, plain Python structures (like a dictionary of booleans) and only lazily instantiate the associated `ctk.BooleanVar` widgets within the active rendering loop (e.g., when a subset of rows is created via pagination). Handlers should immediately sync variables back to the dictionary state.
