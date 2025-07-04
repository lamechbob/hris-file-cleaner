# Logging Strategy

This document outlines how logging is used throughout the HRIS File Cleaner to track process stages, data issues, and critical errors.

---

## 🧭 Purpose of Logging

Logging serves as both a debugging aid and an audit trail. It allows developers and stakeholders to:

- Monitor the flow of data through the system
- Identify which records were altered, skipped, or failed
- Trace operational issues without halting execution

---

## 📶 Logging Levels

| Level    | Purpose                                                                 |
|----------|-------------------------------------------------------------------------|
| `INFO`   | Used for high-level updates and counts (e.g., total records processed)  |
| `WARNING`| Used when data issues are found but execution can continue              |
| `ERROR`  | Reserved for critical failures (e.g., unreadable files, bad formats)    |

---

## 🔍 Sample Logging Output

```plaintext
INFO Total records: 20
INFO Phone numbers corrected: 11
INFO Phone numbers already valid: 9
WARNING Found 1 phone number(s) that are still invalid after cleaning
WARNING 
EmployeeID FirstName LastName  PhoneNumber
    M00011  Courtney  Johnson   0842375945
