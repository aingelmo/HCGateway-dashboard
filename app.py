"""Streamlit app for visualizing HCGateway steps data.

Simplified for clarity and maintainability.
"""

import datetime
import logging
import os

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


# --- Date Range Selection ---
def get_date_range() -> tuple[datetime.date, datetime.date]:
    """Return the selected date range (default: last month to today)."""
    today = datetime.datetime.now().astimezone().date()
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
        return date_range
    return today, today


def parse_steps(steps: list[dict]) -> pd.DataFrame | None:
    """Convert raw steps list to DataFrame with date, count, and source."""
    records = []
    for entry in steps:
        date_raw = entry.get("end") or entry.get("start")
        count = entry.get("data", {}).get("count")
        # Format date as DD-MM-YYYY
        date_fmt = None
        if date_raw:
            try:
                date_str = date_raw.replace("Z", "+00:00")
                date_obj = datetime.datetime.fromisoformat(date_str)
                date_fmt = date_obj.strftime("%d-%m-%Y")
            except ValueError:
                date_fmt = date_raw
        source = entry.get("app", "unknown")
        if date_fmt and count is not None:
            records.append({"date": date_fmt, "count": count, "source": source})
    return pd.DataFrame(records) if records else None


# --- API Fetch Logic ---
def fetch_steps_for_range(
    hcg_username: str,
    hcg_password: str,
    start_date: datetime.date,
    end_date: datetime.date,
) -> list[dict]:
    """Fetch steps data from API for the given date range."""
    date_query = {
        "end": {
            "$gte": start_date.strftime("%Y-%m-%dT00:00:00Z"),
            "$lte": end_date.strftime("%Y-%m-%dT23:59:59Z"),
        },
    }
    data = fetch_data("steps", date_query, hcg_username, hcg_password)
    return data if isinstance(data, list) else []


# --- Main App Logic ---
def main() -> None:
    """Run the Streamlit HCGateway Steps Visualizer app.

    Handle user authentication, date range selection, data fetching, and visualization.
    """
    hcg_username, hcg_password, submitted = get_credentials()
    if not submitted:
        return
    if not hcg_username or not hcg_password:
        st.error("Please enter both username and password.")
        return
    try:
        st.info("Attempting to fetch steps from API...")
        start_date, end_date = get_date_range()
        steps = fetch_steps_for_range(hcg_username, hcg_password, start_date, end_date)
        if not steps:
            st.warning("No steps data found. Check the query, credentials, and API connectivity.")
            return
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


if __name__ == "__main__":
    main()
