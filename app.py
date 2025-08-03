"""Streamlit app for visualizing HCGateway steps data.

Simplified for clarity and maintainability.
"""

import logging
import os
from datetime import datetime

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from data_extractor import fetch_data

# --- Logging Config ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
project_logger = logging.getLogger("hcgateway")
project_logger.setLevel(logging.DEBUG)
if not project_logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s"))
    project_logger.addHandler(handler)
logging.getLogger("streamlit").setLevel(logging.INFO)

# --- App Config ---
load_dotenv()
st.set_page_config(page_title="HCGateway Steps Visualizer", layout="centered")
st.title("HCGateway Steps Visualizer")

# --- Constants ---
DATE_RANGE_LENGTH = 2

# --- Credential Handling ---


def get_credentials() -> tuple[str, str, bool]:
    """Get credentials from env or user input."""
    username = os.getenv("HCGATEWAY_USERNAME")
    password = os.getenv("HCGATEWAY_PASSWORD")
    if not username or not password:
        with st.form("login_form"):
            username = st.text_input("Username", key="username")
            password = st.text_input("Password", type="password", key="password")
            submitted = st.form_submit_button("Login and Fetch Steps")
        return username, password, submitted
    return username, password, True


# --- Data Processing ---
def parse_steps(steps: list[dict]) -> pd.DataFrame | None:
    """Convert raw steps list to DataFrame with date, count, and source.

    Args:
        steps (list[dict]): List of step entries.

    Returns:
        pd.DataFrame | None: DataFrame with columns date, count, source, or None if no valid records.

    """
    records = []
    for entry in steps:
        date_raw = entry.get("end") or entry.get("start")
        count = entry.get("data", {}).get("count")
        # Format date as DD-MM-YYYY
        date_fmt = None
        if date_raw:
            try:
                date_str = date_raw.replace("Z", "+00:00")
                date_obj = datetime.fromisoformat(date_str)
                date_fmt = date_obj.strftime("%d-%m-%Y")
            except ValueError:
                date_fmt = date_raw
        source = entry.get("app", "unknown")
        if date_fmt and count is not None:
            records.append({"date": date_fmt, "count": count, "source": source})
    return pd.DataFrame(records) if records else None


# --- Main App Logic ---
hcg_username, hcg_password, submitted = get_credentials()

if submitted:
    if not hcg_username or not hcg_password:
        st.error("Please enter both username and password.")
    else:
        try:
            st.info("Attempting to fetch steps from API...")
            # Date range input with default value of last month
            today = datetime.now().astimezone().date()
            default_end = today
            if today.month == 1:
                default_start = today.replace(year=today.year - 1, month=12)
            else:
                default_start = today.replace(month=today.month - 1)
            min_date = today.replace(year=today.year - 5)
            date_range = st.date_input(
                "Select date range",
                value=(default_start, default_end),
                min_value=min_date,
                max_value=today,
            )
            if isinstance(date_range, tuple) and len(date_range) == DATE_RANGE_LENGTH:
                start_date, end_date = date_range
            else:
                start_date = end_date = today
            # Build date_query from slider
            date_query = {
                "end": {
                    "$gte": start_date.strftime("%Y-%m-%dT00:00:00Z"),
                    "$lte": end_date.strftime("%Y-%m-%dT23:59:59Z"),
                },
            }
            data = fetch_data("steps", date_query, hcg_username, hcg_password)
            steps = data if isinstance(data, list) else []
            if not steps:
                st.warning("No steps data found. Check the query, credentials, and API connectivity.")
            else:
                st.success("Steps data fetched successfully.")
                df = parse_steps(steps)
                if df is not None:
                    st.line_chart(df.set_index("date")["count"])
                    st.dataframe(df)
                else:
                    st.warning("No valid step records to display.")
        except (KeyError, ValueError, TypeError) as e:
            st.error(f"Failed to fetch steps: {e}")
        except RuntimeError:
            st.error("A runtime error occurred. Please try again later.")
            st.stop()
