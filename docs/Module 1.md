# Role & Context
Act as a Senior Desktop Application Developer and UI/UX Expert. We are building a modern, highly polished desktop application called "Instagram Auditor". 

Your task is to write the complete, production-ready Python code for **Module 1: Data Upload & Quick Analysis**.

# Tech Stack & Architecture
* **Language:** Python 3.10+
* **GUI Framework:** `customtkinter` (Latest version).
* **Libraries:** `json` (for parsing), `webbrowser` (for links), `tkinter.filedialog` (for file selection), `os` (for path handling).
* **Architecture Pattern:** Use Object-Oriented Programming (OOP). Structure the UI using a component-based approach (similar to React). Create a main `App` class that inherits from `ctk.CTk`, and separate classes for `Screen1_Upload` and `Screen2_Results` that inherit from `ctk.CTkFrame`. Manage state seamlessly to destroy/hide the old frame and pack the new one during screen transitions.

# UI/UX Global Design System
* **Theme:** Dark mode by default (`ctk.set_appearance_mode("dark")`).
* **Color Palette:** Use a sleek blue theme (`ctk.set_default_color_theme("blue")`), but utilize red text/accents for negative results (e.g., the "Traitors" count) and green for positive stats.
* **Window Size:** 850x650. Non-resizable if possible to maintain perfect layout proportions.
* **Typography:** Use modern, clean fonts (e.g., "Helvetica" or "Segoe UI"). Use larger font sizes for headings and hero statistics.
* **Padding:** Use generous, consistent padding (`padx=20, pady=20`) to avoid a cramped "Windows 95" look.

---

# Functional Requirements & Screen Flow

## Screen 1: The "Education" Dashboard
This is the landing screen. It must educate the user and collect the files.
1.  **Main Header:** A large, bold, centered title: "Instagram Auditor".
2.  **Instruction Card (Center):** A visually distinct frame containing a step-by-step guide formatted clearly:
    * *Title:* "How to get your JSON files safely:"
    * *Step 1:* Go to Accounts Center -> Your Information and Permissions.
    * *Step 2:* Click 'Download your information'.
    * *Step 3:* Select ONLY 'Followers and following' (to save time).
    * *Step 4:* **Crucial:** Set format to JSON, Date Range to 'All Time'.
3.  **Action Button:** A prominent button labeled `[ Open Instagram Settings ]` that executes `webbrowser.open("https://accountscenter.instagram.com/info_and_permissions/dyi/")`.
4.  **Upload Section:** Two distinct rows for file uploads.
    * Row 1: A label showing the current file status (default: "followers_1.json not selected"), and a button `[ Select Followers ]`.
    * Row 2: A label showing the current file status (default: "following.json not selected"), and a button `[ Select Following ]`.
    * *Dynamic UX:* When a file is successfully loaded via `filedialog`, truncate the path so it looks clean, turn the label text Green, and append a checkmark (✓).
5.  **Proceed Button:** A large, centered button at the bottom: `[ Analyze Data ]`. This button must be **disabled** by default, and only become **enabled/clickable** once both file variables are populated.

## Logic Module: The Parser
When `[ Analyze Data ]` is clicked, run this logic before transitioning to Screen 2:
1.  Read both JSON files. 
2.  *Robust Parsing:* Instagram's JSON structure changes frequently. Safely traverse the JSON. Look for usernames typically nested under `string_list_data[0]['value']`.
3.  Create two Python `set()` objects: `following_set` and `followers_set`.
4.  Calculate the Traitors: `traitors_list = list(following_set - followers_set)`.
5.  *Error Handling:* Wrap this in a try-except block. If parsing fails or files are invalid, spawn a `CTkToplevel` error popup saying "Invalid JSON format. Please ensure you downloaded the correct Instagram data."

## Screen 2: The Quick Analysis (Step 1 Results)
If parsing is successful, destroy/hide Screen 1 and display Screen 2.
1.  **Header:** "Quick Analysis Complete".
2.  **Summary Statistics:** Display two small info cards or labels side-by-side:
    * "You follow: [X] accounts"
    * "Accounts following you: [Y]"
3.  **Hero Statistic (The Hook):** A massive, bold, visually striking text block in the center:
    * **"Found [Z] people who don't follow you back."** (Make the number [Z] red and very large).
4.  **Choice Action Area:** Two massive, equally sized buttons at the bottom.
    * **Button 1 (Left):** `[ Export List & Exit ]`. 
        * *Action:* Opens a `filedialog.asksaveasfilename` (defaulting to `traitors.txt`). Writes the `traitors_list` to the text file, one username per line. Shows a success popup, then runs `app.quit()`.
    * **Button 2 (Right, Primary Color):** `[ Deep Scan (Identify Influencers) ]`.
        * *Subtitle/Tooltip under button:* "Requires a burner account to filter out verified/famous accounts."
        * *Action:* For now, this is a stub. It should print "Transitioning to Module 2..." to the terminal and show an informational popup saying "Module 2: Burner Setup coming soon."

# Output Rules
Provide the entire, runnable Python code in a single code block. Ensure it includes generous comments explaining the logic, especially the state-management between screens and where Module 2 will easily plug in later.
