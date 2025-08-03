"""Steps data processing module for HCGateway dashboard."""

import datetime

import pandas as pd
import streamlit as st

import data_extractor
from models.steps import validate_steps_list


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


def steps_visualizer(hcg_username: str, hcg_password: str, start_date: datetime.date, end_date: datetime.date) -> None:
    """Visualize steps data."""
    try:
        st.info("Attempting to fetch steps from API...")
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
