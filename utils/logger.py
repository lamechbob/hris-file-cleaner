# --------------------
# Core Python Packages
# --------------------
import os
import logging

# --------------------
# Third-Party Packages
# --------------------
import pandas as pd

# --------------------
# Project Modules
# --------------------
from locators.settings import Settings as st

# Ensure the log directory exists
os.makedirs(st.LOG_PATH, exist_ok=True)

# Build log file name using calendar label and current date
log_filename = f"{st.LOG_PATH}/HRI_PHONE_REVIEW_{pd.to_datetime('today').strftime('%m%d%Y')}.log"

# Configure logging: set output file, format, and mode
logging.basicConfig(
    filename=log_filename,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='w'  # Overwrites file on each run. Use 'a' to append.
)

# Get the default logger instance and set debug level
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
