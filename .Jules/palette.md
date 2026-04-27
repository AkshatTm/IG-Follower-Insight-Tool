## 2024-05-18 - Clickable Rows for Toggle Switches
**Learning:** In lists with toggle switches (like the Smart Filter Dashboard), users naturally try to click the row text or empty space rather than aiming for the small switch widget itself. Making the entire row a click target significantly improves the UX by making it more forgiving and accessible.
**Action:** When implementing lists with per-row boolean toggles, bind click events to the row container and primary text labels to toggle the underlying state, and provide visual feedback by setting the cursor to a pointer (e.g., `cursor="hand2"` in Tkinter/CustomTkinter).

## 2024-05-19 - Adding Empty States for Filter Searches
**Learning:** In lists with real-time search filtering, returning a blank scrollable area when no items match the query is poor UX and can lead users to think the application is broken.
**Action:** Always include an empty state message (e.g. "No users found matching your search.") in scrollable/filterable lists. In CustomTkinter, this can be implemented by managing the visibility of a generic `ctk.CTkLabel` using `pack()` to show and `pack_forget()` to hide based on search results.
