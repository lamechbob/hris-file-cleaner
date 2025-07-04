# --------------------
# Core Python Packages
# --------------------
import os
import re
import datetime

# --------------------
# Third-Party Packages
# --------------------
import pandas as pd

# --------------------
# Project Modules
# --------------------
from locators.settings import Settings as st
from extract.extract_hris_file import ExtractHrisFile as ehf
from transform.transform_hris_file import TransformHrisFile as thf
from load.save_transformed_hris import SaveTransformedHRIS as sth
from load.save_hris_report import SaveCorrectionReport as scr

# --------------------
# Application Entry Point
# --------------------

# Step 1: Load the latest HRIS file
print('Loading latest HRIS file...')
extractor = ehf()
hris_data = extractor.load_hris_data()
print('HRIS file loaded.\n')

# Step 2: Display preview of raw data
print('Raw HRIS Data Preview:')
print(hris_data.head())
print('\n')

# Step 3: Run transformations
print('Running phone number cleanup...')
transformer = thf(hris_data)
transformer.run_all()
print('Phone number cleanup complete.\n')

# Step 4: Display preview of transformed data
transformed_hris_data = transformer.get_transformed_hris()
print('Transformed HRIS Data Preview:')
print(transformed_hris_data.head())

# Step 5: Save altered HRIS file
print('Saving altered HRIS file...')
sth_object = sth(transformed_hris_data, extractor.get_file_name())
sth_object.save_file()
print('Altered HRIS file saved.\n')

# Step 6: Save correction report
print('Saving correction report...')
scr_object = scr(transformer.get_corrected_records(), extractor.get_file_name())
scr_object.save_to_excel()
print('Correction report saved.\n')

