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

## 2024-05-18 - Strict Sanitization at Parsing Layer
**Vulnerability:** Extracted usernames from JSON files were not strictly sanitized before being stored in the app state. This allowed users to potentially inject characters that bypass later checks or cause issues in CSV export (Format/CSV Injection) if the earlier defense in `screen_export.py` was flawed.
**Learning:** It's safer to neutralize malicious input as close to the source (the parser) as possible using an allowlist approach, rather than relying solely on escaping later in the pipeline.
**Prevention:** Strictly sanitize parsed data using an allowlist (e.g., `re.sub(r'[^a-zA-Z0-9._]', '', username)`) to ensure downstream components only ever handle clean data.
