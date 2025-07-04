# HRIS File Format Specification

This document defines the expected structure, formatting, and rules for the incoming HRIS census file used in the phone number cleanup project.

---

## 🔍 Expected Columns (in order)

| Column Name       | Type        | Description |
|-------------------|-------------|-------------|
| EffectiveDate     | Date (YYYY-MM-DD) | The date on which this row becomes active for system processing |
| EmployeeID        | String      | Unique employee identifier |
| FirstName         | String      | Legal first name |
| LastName          | String      | Legal last name |
| DateOfBirth       | Date (YYYY-MM-DD) | Must be a valid past date |
| PhoneNumber       | String      | Must be U.S.-formatted (see rule below) |
| Email             | String      | Must contain `@` and domain |
| EmploymentStatus  | String      | One of: `Active`, `Terminated`, `Leave` |
| HireDate          | Date (YYYY-MM-DD) | Cannot be in the future |
| TerminationDate   | Date or Blank | Required if status is `Terminated`; otherwise blank |
| Department        | String      | Optional department label (e.g., HR, IT, Sales) |

---

## ☎️ Phone Number Format Rule

Phone numbers must follow a valid U.S. format:

- Examples: `(305) 555-1234`, `305-555-1234`, `3055551234`
- International numbers like `+44`, `+234` must be converted to U.S. format when possible
- Non-convertible values will be flagged in the validation log

---

## 📌 Employment Status Rules

- If `EmploymentStatus` is `Active` or `Leave`: `TerminationDate` must be **blank**
- If `EmploymentStatus` is `Terminated`: `TerminationDate` must be present and **on or after `HireDate`**
- `EffectiveDate` must be equal to or greater than `HireDate`

---

## 🧪 Sample Row

2025-07-02,M0001,John,Doe,1990-01-15,+1 (305) 555-1234,john.doe@email.com,Active,2015-05-20,,IT

---

## 📁 Sample File

- **Filename:** `raw_hris_07022025.csv`
- **Row count:** 10
- **Encoding:** `utf-8-sig` (Excel compatible)
