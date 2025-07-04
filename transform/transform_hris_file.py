# --------------------
# Core Python Packages
# --------------------
import logging
import os
import re
from datetime import datetime

# --------------------
# Third-Party Packages
# --------------------
import pandas as pd

# --------------------
# Project Modules
# --------------------
from locators.settings import Settings as st
from utils.logger import logger

class TransformHrisFile:

    def __init__(self,hris_data):

        # Logging
        self.logger = logging.getLogger()

        logger.info('-- Transforming HRIS File Data')

        # Raw HRIS data passed from the Extract phase
        self.hris_data = hris_data

        # Placeholder for corrected records
        self.corrected_records = pd.DataFrame(columns=[
            'EmployeeID', 'FirstName', 'LastName', 'PhoneNumber', 'Action', 'Reason'
        ])
    def clean_phone_numbers(self):

        # Step 1: Convert the PhoneNumber column to string and strip all non-digit characters (e.g., +, -, (), spaces)
        # Step 2: For numbers that are 11 digits and begin with '1', treat them as U.S. international format and remove the leading '1'
        # Step 3: Identify phone numbers that were already valid (original had 10 digits after removing formatting)
        # Step 4: Identify phone numbers that were corrected (changed from original and now exactly 10 digits)
        # Step 5: Identify any phone numbers that are still invalid (not 10 digits even after cleaning)
        # Step 6: If any phone numbers remain invalid, log those records for inspection
        # Step 7: Overwrite the PhoneNumber column with cleaned values
        # Step 8: Log summary statistics for total, corrected, valid, and invalid phone numbers
        # Step 9: If corrections were made, log the affected employee records (EmployeeID, FirstName, LastName, PhoneNumber)

        # Create a Series of phone numbers as strings (preserves original formatting for comparison)
        original = self.hris_data['PhoneNumber'].astype(str)

        # Remove all non-digit characters (e.g., +, -, (), spaces) to isolate numeric phone values
        digits_only = original.str.replace(r'\D', '', regex=True)

        # If the phone number is exactly 11 digits and starts with '1',
        # assume it's a U.S. number in international format and remove the leading '1'
        # (e.g., +13055551234 → 3055551234).
        # All other numbers are left unchanged, even if they are not valid U.S. formats.
        cleaned = digits_only.where(~((digits_only.str.len() == 11) & digits_only.str.startswith('1')),
                                    digits_only.str[1:])

        # A number is considered already valid if:
        #   - Its cleaned version matches the stripped original
        #   - AND it's exactly 10 digits long
        already_valid = (digits_only == cleaned) & (cleaned.str.len() == 10)

        # A number is considered corrected if:
        #   - It was NOT already valid (i.e., formatting or a leading '1' needed to be removed)
        #   - AND the cleaned version is now a valid 10-digit number
        # This ensures we only count as "corrected" those numbers that required transformation and are now valid
        corrected = (~already_valid) & (cleaned.str.len() == 10)
        new_corrections = self.hris_data.loc[corrected, ['EmployeeID', 'FirstName', 'LastName', 'PhoneNumber']]

        # Define metadata for this specific data transformation
        correction_action = 'Changed'
        correction_reason = 'Stripped leading 1 or removed formatting from phone number'

        # Add metadata
        new_corrections['Action'] = correction_action
        new_corrections['Reason'] = correction_reason

        self.corrected_records = pd.concat([self.corrected_records, new_corrections], ignore_index=True)

        # Identify records that are still invalid after cleaning;
        # we assume any phone number not exactly 10 digits is invalid under U.S. formatting rules
        still_invalid = cleaned.str.len() != 10

        # Identify and log any records that still have invalid phone numbers after cleaning
        if still_invalid.any():

            # Filter and extract details of invalid records for logging
            invalid_records = self.hris_data.loc[still_invalid, ['EmployeeID', 'FirstName', 'LastName', 'PhoneNumber']]

            # Log the total number of records that remain invalid
            logger.warning(f'Found {still_invalid.sum()} phone numbers that are still invalid after cleaning.')

            # Log the full details of each invalid record for review
            logger.warning('\n' + invalid_records.to_string(index=False))

        # Update the 'PhoneNumber' column in the HRIS data with the cleaned 10-digit values
        # (international prefixes and formatting removed)
        self.hris_data['PhoneNumber'] = cleaned

        # Log summary statistics:
        # - Total number of records processed
        # - Count of phone numbers that were corrected
        # - Count of phone numbers that were already in a valid format
        # logger.info(f'Total records: {len(self.hris_data)}')
        self.logger.info(f'Phone numbers corrected: {corrected.sum()}')
        self.logger.info(f'Phone numbers already valid: {already_valid.sum()}')

        # Log details of employees whose phone numbers were corrected
        # Includes EmployeeID, FirstName, LastName, and the updated PhoneNumber
        # If no corrections occurred, log a confirmation message
        if not new_corrections.empty:
            self.logger.info('Corrected phone numbers for the following employees:')
            self.logger.info('\n' + new_corrections.to_string(index=False))
        else:
            self.logger.info('No phone numbers required correction.')

    def get_transformed_hris(self):
        return self.hris_data

    def get_corrected_records(self):
        return self.corrected_records

    def run_all(self):
        # Orchestrator: runs all transformation methods in order
        self.clean_phone_numbers()
        # Add more methods here as needed