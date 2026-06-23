## 2024-04-25 - Prevent CSV Injection in Export Feature
**Vulnerability:** The application exports a list of usernames to a CSV file without sanitizing the data. Usernames starting with characters like `=, +, -, @` could be executed as formulas if the CSV is opened in spreadsheet software (Excel, Google Sheets), leading to Formula Injection (CSV Injection) attacks.
**Learning:** Even internal tool data (like usernames) must be sanitized when exported to formats like CSV, as external applications parsing the data may evaluate certain characters as executable code.
**Prevention:** Always check user-controlled data before writing to a CSV. Prepend a single quote (`'`) to any string starting with `=`, `+`, `-`, or `@` to force the spreadsheet application to treat the field as plain text.

## 2024-04-27 - Prevent DoS via Large Files and Long Strings in UI
**Vulnerability:** The application was vulnerable to Denial of Service (DoS) attacks on two fronts: memory exhaustion by parsing excessively large JSON files, and UI freezing caused by rendering artificially massive strings in CustomTkinter.
**Learning:** Desktop applications handling local, user-provided files are susceptible to DoS if they lack bounds checking. Loading a 2GB JSON file into memory, or passing a 1MB long username string to a UI widget, can easily freeze or crash the entire application thread.
**Prevention:** Always implement hard limits on input size. Check file sizes (e.g., `os.path.getsize()`) before attempting to parse them into memory. Enforce strict character limits on strings (e.g., username length) before they are passed to the UI layer.
## 2026-04-26 - [Error Message Information Leakage]
**Vulnerability:** The application was exposing raw exception messages (`str(e)`) to the UI via `ToastPopup` upon export and parsing failures in `screen_export.py`, `screen_results.py`, and `screen_upload.py`.
**Learning:** This could leak sensitive system information such as directory structures and local file paths (e.g., if a `FileNotFoundError` occurs during export, the full path is shown to the user).
**Prevention:** Catch exceptions and log them using a secure backend mechanism (like `print` for a CLI or a logging framework), while displaying a generic, sanitized, user-friendly error message in the UI instead.
## 2024-05-18 - File Size Bypass via Character Devices
**Vulnerability:** The application used `os.path.getsize(filepath)` to check if a file was too large (to prevent memory exhaustion DoS) before parsing it as JSON. However, special files like character devices (e.g., `/dev/zero`) return a size of `0` from `os.path.getsize()`, effectively bypassing the size check, but when read, they produce an infinite stream of data, leading to a Denial of Service.
**Learning:** `os.path.getsize()` is insufficient for preventing DoS attacks when reading files. It does not account for infinite streams produced by non-regular files like character devices or named pipes which report a size of 0.
**Prevention:** Always explicitly check if a given path is a regular file using `os.path.isfile(filepath)` before reading its contents, especially before attempting to load the entire contents into memory.

## 2026-05-04 - Fix Memory Exhaustion Bypass via Character Devices
**Vulnerability:** The memory exhaustion check in `src/parser.py` relied on `os.path.getsize()` to prevent DoS attacks via excessively large JSON files. However, `os.path.getsize()` returns `0` for character devices like `/dev/zero`, allowing the check to be bypassed and leading to infinite memory consumption when reading the file.
**Learning:** Character devices have a size of 0 but can produce infinite streams of data. Relying solely on file size checks without verifying file types opens the door to DoS attacks on local applications.
**Prevention:** Always verify that a file path points to a regular file using `os.path.isfile()` before performing operations like size checks or reading data into memory.
## 2024-05-03 - Prevent DoS via Infinite Stream Devices in Parser
**Vulnerability:** The application used `os.path.getsize()` to check file sizes prior to parsing JSON files as a DoS mitigation. However, character device files (like `/dev/zero` or `/dev/urandom`) return a size of `0` in Python, bypassing the size check limit. Parsing such files via `json.load()` causes an infinite read operation that quickly exhausts system memory, leading to a Denial of Service.
**Learning:** `os.path.getsize()` cannot be fully trusted as the sole DoS mitigation against massive files if the input could be a device stream instead of a regular file on disk.
**Prevention:** Always verify `os.path.isfile(filepath)` alongside size checks when accepting user-provided local file paths to ensure the application is only attempting to parse regular files.
## 2026-05-02 - Prevent CSV/Formula Injection during .txt Export
**Vulnerability:** The application was exporting a list of non-followers directly to a `.txt` file. If a username started with a character like `=`, `+`, `-`, or `@`, and the `.txt` file was imported into spreadsheet software like Excel, it could be executed as a formula, leading to CSV/Formula Injection.
**Learning:** Even simple `.txt` exports can be vulnerable to formula injection if the intent is for users to import the data into spreadsheets or databases. Mitigation must be applied at the export boundary, not by destructively stripping valid characters at parse time.
**Prevention:** Always prepend a single quote (`'`) to strings that begin with `=`, `+`, `-`, or `@` when generating files meant to be imported into spreadsheet applications.

## 2026-05-04 - Prevent Information Leakage via Error Messages
**Vulnerability:** The application was exposing raw exception messages (`str(e)`) to the UI in `screen_upload.py`, which could leak sensitive internal system information such as local file paths if an unexpected error occurred during parsing.
**Learning:** Raw exception details should only be logged internally (e.g., printed to the console). Displaying them to end-users via UI popups creates an information leakage vulnerability.
**Prevention:** Catch exceptions, log the detailed error internally, and present a static, safe, generic error message to the user in the UI.
