"""Dashboard components for HCGateway steps visualization."""

import datetime
from typing import Any, cast

import pandas as pd
import streamlit as st

from hcgateway_dashboard.api_client import HCGatewayClient
from hcgateway_dashboard.config import DATE_RANGE_LENGTH, HCGATEWAY_PASSWORD, HCGATEWAY_USERNAME
from hcgateway_dashboard.models.steps import validate_steps_list


class Dashboard:
    """Main dashboard class for HCGateway steps visualization."""

    def __init__(self) -> None:
        """Initialize dashboard with API client."""
        self.client = HCGatewayClient()

    def get_credentials(self) -> tuple[str, str, bool]:
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

    def get_date_range(self) -> tuple[datetime.date, datetime.date]:
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
        if (
            isinstance(date_range, tuple)
            and len(date_range) == DATE_RANGE_LENGTH
            and all(isinstance(d, datetime.date) for d in date_range)
        ):
            # Use cast to tell MyPy we have exactly tuple[date, date]
            date_tuple = cast("tuple[datetime.date, datetime.date]", date_range)
            return date_tuple[0], date_tuple[1]
        return today, today

    def parse_steps(self, steps: list[dict[str, Any]]) -> pd.DataFrame | None:
        """Convert raw steps list to DataFrame with date, count, and source."""
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
        self,
        username: str,
        password: str,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> list[dict[str, Any]]:
        """Fetch steps data from API for the given date range."""
        date_query = {
            "end": {
                "$gte": start_date.strftime("%Y-%m-%dT00:00:00Z"),
                "$lte": end_date.strftime("%Y-%m-%dT23:59:59Z"),
            },
        }

        try:
            response = self.client.fetch_data("steps", date_query, username, password)
            # Extract the actual data from the response
            data = response.get("data", []) if isinstance(response, dict) else []
            if not isinstance(data, list):
                return []

            # Validate step data before returning
            validate_steps_list(data)
        except (ValueError, TypeError) as e:
            st.error(f"Step data validation failed: {e}")
            return []
        else:
            return data

    def visualize_steps(
        self,
        username: str,
        password: str,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> None:
        """Visualize steps data."""
        try:
            st.info("Attempting to fetch steps from API...")
            steps = self.fetch_steps_for_range(username, password, start_date, end_date)
            if not steps:
                st.warning(
                    "No steps data found. Check the query, credentials, and API connectivity.",
                )
                return

            st.success("Steps data fetched successfully.")
            steps_dataframe = self.parse_steps(steps)
            if steps_dataframe is not None:
                st.line_chart(steps_dataframe.set_index("date")["count"])
                st.dataframe(steps_dataframe)
            else:
                st.warning("No valid step records to display.")
        except (KeyError, ValueError, TypeError) as e:
            st.error(f"Failed to fetch steps: {e}")
        except RuntimeError:
            st.error("A runtime error occurred. Please try again later.")
            st.stop()

    def run(self) -> None:
        """Run the Streamlit HCGateway Steps Visualizer app."""
        st.set_page_config(page_title="HCGateway Steps Visualizer", layout="centered")
        st.title("HCGateway Steps Visualizer")

        hcg_username, hcg_password, submitted = self.get_credentials()
        if not submitted:
            return
        if not hcg_username or not hcg_password:
            st.error("Please enter both username and password.")
            return

        start_date, end_date = self.get_date_range()
        self.visualize_steps(hcg_username, hcg_password, start_date, end_date)
