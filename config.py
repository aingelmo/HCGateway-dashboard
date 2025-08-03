"""Configuration settings for HCGateway Steps Visualizer app.

This module provides:
- Logging configuration
- Environment variable loading
- Common constants
"""

import logging
import os

from dotenv import load_dotenv

# --- Env Config ---
load_dotenv()


# --- Logging Config ---
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

project_logger = logging.getLogger("hcgateway")
project_logger.setLevel(LOGGING_LEVEL)
if not project_logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    project_logger.addHandler(handler)


# --- Global Environment Variables ---
HCGATEWAY_USERNAME = os.getenv("HCGATEWAY_USERNAME", "")
HCGATEWAY_PASSWORD = os.getenv("HCGATEWAY_PASSWORD", "")

# --- Constants ---
DATE_RANGE_LENGTH = 2
TOKEN_EXPIRY_MARGIN_SECONDS = 300  # 5 minutes
