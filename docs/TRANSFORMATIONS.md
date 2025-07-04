# Data Transformations

This document outlines the transformation logic applied during the HRIS data cleanup process, with a focus on phone number formatting and record classification.

---

## 📞 Phone Number Cleaning Logic

1. **Convert to String**
   - Ensures consistent processing and preserves leading zeros if present.

2. **Strip Non-Digit Characters**
   - Removes characters such as `+`, `-`, spaces, parentheses using regex.
   - Example: `+1 (555) 123-4567` → `15551234567`

3. **Remove Leading '1'**
   - If the cleaned string is 11 digits and starts with `1`, assume it’s a U.S. number with country code.
   - Strip the leading `1` to normalize it to a 10-digit number.
   - Example: `15551234567` → `5551234567`

4. **Validate as U.S. Number**
   - After cleaning, phone numbers must be exactly 10 digits to be considered valid.
   - All other lengths are marked as invalid and flagged in the report.

---

## ✅ Correction Classification Logic

Each record is tagged based on its post-cleaning state:

- **Already Valid**
  - The original phone number was already 10 digits and needed no change.

- **Changed**
  - The phone number was altered (e.g., country code removed or formatting stripped).
  - An "Action" (`Changed`) and "Reason" (e.g., `Stripped leading 1 from phone number`) is added to the audit report.

- **Invalid**
  - The phone number was still not 10 digits after all transformations.
  - These are logged separately and may require manual attention.

---

## 🔄 Scalable Design

- New transformations (e.g., name cleaning, address validation) can follow this same pattern:
  - Isolate original data
  - Apply cleaning logic
  - Compare original vs cleaned
  - Document action + reason if a change was made

---

## 📌 Example Transformations

| Original Phone Number | Cleaned | Action  | Reason                                 |
|------------------------|---------|---------|----------------------------------------|
| `+1 (555) 123-4567`    | `5551234567` | Changed | Stripped leading 1 from phone number   |
| `413-525-6012`         | `4135256012` | Already Valid | -                                  |
| `0842375945`           | `0842375945` | Already Valid | -                                  |
| `1615109032`           | `1615109032` | Invalid | Not a valid 10-digit U.S. number |

