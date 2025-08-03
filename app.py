"""Streamlit app for visualizing HCGateway steps data.

Simplified for clarity and maintainability.
"""

import datetime

import pandas as pd
import streamlit as st

import data_extractor
from config import DATE_RANGE_LENGTH, HCGATEWAY_PASSWORD, HCGATEWAY_USERNAME
from models.steps import validate_steps_list

st.set_page_config(page_title="HCGateway Steps Visualizer", layout="centered")
st.title("HCGateway Steps Visualizer")


# --- Credential Handling ---
def get_credentials() -> tuple[str, str, bool]:
    """Get credentials from config or user input."""
    username = HCGATEWAY_USERNAME
    password = HCGATEWAY_PASSWORD
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
    """Convert raw steps list to DataFrame with date, count, and source. Validates using StepsRecord."""
    try:
        validated = validate_steps_list(steps)
    except (ValueError, TypeError) as e:
        st.error(f"Step data validation failed: {e}")
        return None
    records = []
    for entry in validated:
        dt_obj = entry.end_dt or entry.start_dt
        count = entry.data.count
        date_fmt = dt_obj.strftime("%d-%m-%Y") if dt_obj else None
        source = entry.app or "unknown"
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
    """Fetch steps data from API for the given date range. Validates using StepsRecord."""
    date_query = {
        "end": {
            "$gte": start_date.strftime("%Y-%m-%dT00:00:00Z"),
            "$lte": end_date.strftime("%Y-%m-%dT23:59:59Z"),
        },
    }
    data = data_extractor.fetch_data("steps", date_query, hcg_username, hcg_password)
    if not isinstance(data, list):
        return []
    # Validate step data before returning
    try:
        validate_steps_list(data)
    except (ValueError, TypeError) as e:
        st.error(f"Step data validation failed: {e}")
        return []
    return data


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
