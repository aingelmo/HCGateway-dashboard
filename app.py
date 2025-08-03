"""Streamlit app for visualizing HCGateway steps data.

Simplified for clarity and maintainability.
"""

import os
from datetime import datetime

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from data_extractor import fetch_data

# --- App Config ---
load_dotenv()
st.set_page_config(page_title="HCGateway Steps Visualizer", layout="centered")
st.title("HCGateway Steps Visualizer")


# --- Credential Handling ---
def get_credentials() -> tuple[str, str, bool]:
    """Get credentials from env or user input.

    Returns:
        tuple: (username, password, submitted)

    """
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
            data = fetch_data("steps", {}, hcg_username, hcg_password)
            steps = data if isinstance(data, list) else []
            if not steps:
                st.warning("No steps data found.")
            else:
                st.success("Steps data fetched successfully.")
                st.write("Raw Data:", steps)
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
