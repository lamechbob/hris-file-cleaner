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

class ExtractHrisFile:

    def __init__(self):

        logger.info('-- Extracting HRIS File Data')

        self.directory = st.ORIGINAL_HRIS_DIRECTORY # Directory where raw HRIS files are stored

        # Initialize a placeholder to store the name of the most recently loaded HRIS file.
        # This will be useful for downstream tasks such as naming outputs or audit logging.
        self.file_name  = ''

        logger.info(f'Directory: {self.directory}')

    def load_hris_data(self):

        # Pattern: matches files using the naming convention raw_hris_MMDDYYYY.csv (e.g., raw_hris_07022025.csv)
        pattern = re.compile(r"raw_hris_(\d{8})\.csv")

        latest_date = None  # Date extracted from the most recent file name
        latest_file = None  # Filename corresponding to the latest date

        # This block iterates through all files in the directory.
        # If a file matches the expected naming convention, it attempts to extract the date.
        # If the extracted date is more recent than the current latest,
        # then latest_date and latest_file are updated accordingly.

        for filename in os.listdir(self.directory):
            match = pattern.match(filename)
            if match:
                file_date_str = match.group(1)
                try:
                    file_date = datetime.strptime(file_date_str, '%m%d%Y')
                    if not latest_date or file_date > latest_date:
                        latest_date = file_date
                        latest_file = filename
                except ValueError:
                    logger.error(f'Bad Date Format: {filename}')
                    continue  # Skip bad date formats

        if not latest_file:
            logger.error('No properly formatted HRIS file found.')
            raise FileNotFoundError('No properly formatted HRIS file found.')

        # Add latest file name
        self.file_name = latest_file

        # Full path example: data/hris_files/raw_hris_MMDDYYYY.csv
        full_path = os.path.join(self.directory, latest_file)

        logger.info(f'Loading latest file by date: {latest_file}')

        # HRIS data extracted from file
        hris_data = pd.read_csv(full_path, encoding='utf-8-sig',dtype=str)
        logging.info(f'Total Records: {len(hris_data.index)}')

        return hris_data

    def get_file_name(self):
        return self.file_name