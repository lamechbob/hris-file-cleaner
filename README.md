# HRIS File Cleaner

A modular ETL-style Python application that reads raw HRIS data, transforms phone numbers into a clean and valid U.S. format, and outputs both an updated data file and an audit report of modifications.

## ❗ Problem Statement

The client’s HRIS system frequently included U.S. phone numbers with a leading `+1` (e.g., `+1 (800) 555-1212`). This format was historically accepted by downstream systems—until one day, employees began experiencing critical issues during the enrollment process.

Without warning, users were unable to advance past a specific enrollment page unless they manually altered their phone number. After investigation, the issue was traced back to phone number formatting. The product team confirmed no changes would be made on the platform side, placing the responsibility on our team to proactively clean the data.

This application was created as a scalable, auditable solution to sanitize phone numbers, identify records requiring correction, and ensure data integrity without relying on manual intervention.

## ✨ Features

- Extracts latest HRIS CSV from configured directory
- Cleans and standardizes phone numbers
- Logs and reports corrected and unfixable phone records
- Exports transformed HRIS file with `_altered` suffix
- Generates Excel audit report of changes (with reasons)

## 🚀 Quick Start

```bash
# Clone the repo
$ git clone https://github.com/yourusername/hris-cleaner.git
$ cd hris-cleaner

# Set up environment
$ pip install -r requirements.txt

# Run the application
$ python app.py
