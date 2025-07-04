# --------------------
# Core Python Packages
# --------------------
import os

# --------------------
# Third-Party Packages
# --------------------
import pandas as pd

# --------------------
# Project Modules
# --------------------
from locators.settings import Settings as st
from utils.logger import logger


class SaveCorrectionReport:

    def __init__(self, corrected_records: pd.DataFrame, original_filename: str):

        self.corrected_records = corrected_records
        self.original_filename = original_filename
        self.output_dir = st.REPORTS_DIRECTORY  # e.g., "./output/reports"

    def save_to_excel(self):

        # Create the output directory if it doesn’t exist
        os.makedirs(self.output_dir, exist_ok=True)

        # Generate report filename
        output_filename = self.generate_report_filename()
        output_path = os.path.join(self.output_dir, output_filename)

        # Save to Excel
        self.corrected_records.to_excel(output_path, index=False)

        # Log the result
        logger.info(f'Correction report saved to: {output_path}')

    def generate_report_filename(self) -> str:

        name_parts = os.path.splitext(self.original_filename)
        base = name_parts[0]

        return f'{base}_corrections.xlsx'
