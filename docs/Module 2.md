### PROJECT: Instagram Auditor App - Module 2 (Deep Scan & Management)

**Role:** You are an expert Python developer specializing in `CustomTkinter` and Data Structures.
**Context:** We are building an "Instagram Auditor" desktop app.
* **Module 1 (Completed):** Handles the JSON file upload, calculates the "Non-Followers" (Set Difference: `Following - Followers`), and displays a basic count on Screen 2.
* **Current State:** The user has clicked the **"Deep Scan (Identify Influencers)"** button on Screen 2.
* **Data Availability:** You have access to the `non_followers` set (a list of strings) generated in Module 1.

**Task:**
Write the Python code for **Module 2**, which acts as the "Manager & Export" engine. This module must seamlessly integrate into the same `App` class as Module 1. It consists of **Screen 3** and **Screen 4**.

---

### SCREEN 3: The "Smart Filter" Dashboard
**Goal:** Allow the user to manually filter the raw "Non-Followers" list to separate "bad" unfollowers from "VIPs/Influencers" (users you want to keep following even if they don't follow back).

**1. UI Layout Requirements:**
* **Header:** Title "Filter Your List" with a dynamic subtitle: "Showing [X] users who don't follow you back."
* **Search Bar:** A `CTkEntry` at the top to filter the scrollable list by username in real-time.
* **The List (Main Feature):** A `CTkScrollableFrame` that occupies most of the screen.
    * Populate this frame with rows corresponding to the `non_followers` list.
    * **Row Design:** Each row must have:
        * **Username Label:** Aligned left.
        * **"Whitelist/VIP" Switch:** A `CTkSwitch` or `CTkCheckBox`. If checked, this user is marked as "Safe" and removed from the "To Unfollow" count.
* **Footer Action Bar:**
    * **"Select/Deselect All" Button:** To quickly toggle the whole list.
    * **"Next: Review & Export" Button:** Moves to Screen 4.

**2. Logic & Persistence (Crucial):**
* **Whitelist File:** On initialization, the app must try to read a local file named `whitelist.json`.
* **Auto-Check:** When populating the list, if a username exists in `whitelist.json`, their "VIP Switch" should be automatically turned **ON** by default.
* **Save State:** When the user clicks "Next," save the current state of all "VIP" users back to `whitelist.json`. This ensures the user doesn't have to re-select their favorite celebrities every time they run the app.

---

### SCREEN 4: The Action Station (Export)
**Goal:** Present the final clean list and provide export options.

**1. UI Layout Requirements:**
* **Summary Stats:** A large, clear label: "Final Count: [X] Users to Unfollow." (This count = Total Non-Followers minus Whitelisted VIPs).
* **Export Tools:**
    * **"Download .CSV" Button:** Opens a file dialog to save the final list as a `.csv` file (Header: "Username", "Status").
    * **"Copy to Clipboard" Button:** Copies the clean list of usernames to the system clipboard (one per line) for easy pasting.
* **Navigation:**
    * **"Restart" Button:** Clears all data and returns the user to Screen 1 (Home).

---

### Technical Constraints
1.  **Library:** Use `customtkinter` exclusively for all UI elements.
2.  **Integration:** The code must be written as methods within the main `App` class (e.g., `def build_screen_3(self):`) or as a dedicated class that modifies the main window.
3.  **Variable Scope:** Ensure the `non_followers` set is passed correctly from Module 1.
4.  **Error Handling:**
    * Handle cases where `whitelist.json` does not exist yet (create it).
    * Handle empty lists (if everyone is whitelisted, show "0 Users to Unfollow").

**Output:**
Provide the complete, functional Python code for Screen 3 and Screen 4, including the JSON read/write logic for the whitelist.
