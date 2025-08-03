"""Streamlit app for visualizing HCGateway steps data.

Simplified for clarity and maintainability.
"""

import datetime

import streamlit as st

from config import DATE_RANGE_LENGTH, HCGATEWAY_PASSWORD, HCGATEWAY_USERNAME
from steps import steps_visualizer

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

    start_date, end_date = get_date_range()

    steps_visualizer(hcg_username, hcg_password, start_date, end_date)


if __name__ == "__main__":
    main()
