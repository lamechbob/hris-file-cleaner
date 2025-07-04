# Data Flow Overview

This document outlines the step-by-step flow of data through the HRIS File Cleaner application.

---

## 1. Extraction

- The system looks for the most recent `.csv` file in the configured input directory.
- Filenames are assumed to contain timestamps or follow consistent naming patterns.
- The selected file is loaded into a Pandas DataFrame.
- The file name is also saved internally for later use in naming output files.

---

## 2. Transformation

- Phone numbers are first converted to strings to preserve formatting.
- All non-digit characters (e.g., `+`, `-`, `(`, `)`, spaces) are stripped.
- If a number is 11 digits and starts with `1`, the leading `1` is removed (U.S. country code).
- Records are classified as:
  - Already valid (exactly 10 digits before cleaning)
  - Corrected (valid after formatting)
  - Still invalid (not 10 digits even after cleaning)
- Corrections are logged, and an audit DataFrame is built that includes:
  - Employee name, ID, updated phone number
  - The action taken (e.g., `Changed`)
  - The reason for the change (e.g., `Stripped leading 1 from phone number`)

---

## 3. Output

- A cleaned HRIS `.csv` file is saved to the `output/` directory using the original file name with an `_altered` suffix.
- An Excel audit report is saved to the `reports/` directory.
- Logging messages are printed to the terminal, showing:
  - Total records processed
  - Count of corrected phone numbers
  - Count of already-valid numbers
  - Any remaining invalid records

---

## Future Considerations

- Additional transformations (e.g., name sanitization, regional filtering) can be plugged into the same pipeline.
- The transformation logic is modular and scalable for new validation rules.
