## 2024-04-25 - Prevent CSV Injection in Export Feature
**Vulnerability:** The application exports a list of usernames to a CSV file without sanitizing the data. Usernames starting with characters like `=, +, -, @` could be executed as formulas if the CSV is opened in spreadsheet software (Excel, Google Sheets), leading to Formula Injection (CSV Injection) attacks.
**Learning:** Even internal tool data (like usernames) must be sanitized when exported to formats like CSV, as external applications parsing the data may evaluate certain characters as executable code.
**Prevention:** Always check user-controlled data before writing to a CSV. Prepend a single quote (`'`) to any string starting with `=`, `+`, `-`, or `@` to force the spreadsheet application to treat the field as plain text.
