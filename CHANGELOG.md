# Changelog

All notable changes to this project will be documented in this file.

## [v1.0.0] - 2025-07-04

### Added
- End-to-end ETL pipeline for HRIS data cleanup
- Extraction module to identify and load the most recent HRIS file
- Transformation logic to:
  - Strip non-digit characters from phone numbers
  - Remove leading `+1` from U.S. numbers
  - Flag valid, corrected, and still-invalid numbers
  - Attach reasons and actions for audit logging
- Logging framework with INFO and WARNING levels
- File-saving logic to:
  - Output altered HRIS CSV file with `_altered` suffix
  - Generate Excel audit report of all corrections

### Changed
- N/A

### Fixed
- N/A

---

> Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
