
# --------------------
# Core Python Packages
# --------------------
import logging
import os
import re

# --------------------
# Third-Party Packages
# --------------------
import pandas as pd

# --------------------
# Project Modules
# --------------------
from locators.settings import Settings as st
from utils.logger import logger

class SaveTransformedHRIS:

    def __init__(self, transformed_hris: pd.DataFrame, original_filename: str):

        self.logger = logging.getLogger()
        logger.info('-- Saving Altered HRIS File Data')

        self.transformed_hris = transformed_hris
        self.original_filename = original_filename
        self.output_dir = st.ALTERED_HRIS_DIRECTORY

    def generate_output_filename(self):

        # Generates a new filename for the transformed HRIS file:
        # - Extracts the base name and extension from the original filename (expects .csv format)
        # - Appends "_altered" to the base name to distinguish it from the source file
        # - Raises an error if the original filename does not match the expected pattern
        # This ensures the output file is traceable and avoids overwriting the original.

        name_parts = re.match(r'(.+?)(\.csv)$', self.original_filename)
        if not name_parts:
            raise ValueError('Invalid original filename format.')

        base, ext = name_parts.groups()
        return f'{base}_altered{ext}'

    def save_file(self):

        # Save the transformed HRIS file:
        # Ensures the output directory exists, generates a new file name based on the original
        # (with '_altered' appended), and writes the cleaned data to a CSV file using UTF-8 encoding
        # compatible with Excel. This preserves formatting and structure while maintaining traceability
        # to the original source.

        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, self.generate_output_filename())
        self.transformed_hris.to_csv(output_path, index=False, encoding='utf-8-sig')

        self.logger.info(f'Saved altered HRIS file to: {output_path}')
        return output_path
