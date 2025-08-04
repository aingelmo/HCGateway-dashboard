"""Dashboard components for HCGateway steps visualization."""

import datetime
import logging
from typing import Any, cast

import pandas as pd
import streamlit as st

from hcgateway_dashboard.api_client import HCGatewayClient
from hcgateway_dashboard.config import (
    DATE_RANGE_LENGTH,
    HCGATEWAY_PASSWORD,
    HCGATEWAY_USERNAME,
)
from hcgateway_dashboard.models.steps import validate_steps_list

logger = logging.getLogger("hcgateway.dashboard_client")


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

    @st.cache_data(ttl=300, show_spinner=False)
    def parse_steps(_self, steps: list[dict[str, Any]]) -> pd.DataFrame | None:  # noqa: N805
        """Convert raw steps list to DataFrame with date, count, and source.

        Cached for 5 minutes to avoid reprocessing the same data.
        """
        logger.info("Parsing %d step records into DataFrame", len(steps))

        try:
            validated = validate_steps_list(steps)
        except (ValueError, TypeError) as e:
            logger.exception("Step data validation failed during parsing")
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

        logger.info("Successfully parsed %d valid records", len(records))
        return pd.DataFrame(records) if records else None

    @st.cache_data(ttl=300, show_spinner=False)
    def fetch_steps_for_range(
        _self,  # noqa: N805
        username: str,
        password: str,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> list[dict[str, Any]]:
        """Fetch steps data from API for the given date range.

        Cached for 5 minutes to avoid API overload.
        """
        logger.info("Fetching steps data for range %s to %s", start_date, end_date)

        date_query = {
            "end": {
                "$gte": start_date.strftime("%Y-%m-%dT00:00:00Z"),
                "$lte": end_date.strftime("%Y-%m-%dT23:59:59Z"),
            },
        }

        try:
            response = _self.client.fetch_data("steps", date_query, username, password)
            data = response
            if not isinstance(data, list):
                logger.warning("API response is not a list, returning empty data")
                return []

            validate_steps_list(data)
            logger.info("Successfully fetched %d step records", len(data))
        except (ValueError, TypeError) as e:
            logger.exception("Step data validation failed")
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
        logger.info("Starting visualization for date range %s to %s", start_date, end_date)

        try:
            st.info("Attempting to fetch steps from API...")
            steps = self.fetch_steps_for_range(username, password, start_date, end_date)
            if not steps:
                logger.warning("No steps data found for the specified date range")
                st.warning(
                    "No steps data found. Check the query, credentials, and API connectivity.",
                )
                return

            st.success("Steps data fetched successfully.")
            steps_dataframe = self.parse_steps(steps)
            if steps_dataframe is not None:
                logger.info("Displaying chart and dataframe with %d records", len(steps_dataframe))
                st.line_chart(steps_dataframe.set_index("date")["count"])
                st.dataframe(steps_dataframe)
            else:
                logger.warning("No valid step records to display after parsing")
                st.warning("No valid step records to display.")
        except (KeyError, ValueError, TypeError) as e:
            logger.exception("Failed to fetch steps")
            st.error(f"Failed to fetch steps: {e}")
        except RuntimeError:
            logger.exception("Runtime error occurred during visualization")
            st.error("A runtime error occurred. Please try again later.")
            st.stop()

    def run(self) -> None:
        """Run the Streamlit HCGateway Steps Visualizer app."""
        logger.info("Starting HCGateway Steps Visualizer dashboard")

        st.set_page_config(page_title="HCGateway Steps Visualizer", layout="centered")
        st.title("HCGateway Steps Visualizer")

        hcg_username, hcg_password, submitted = self.get_credentials()
        if not submitted:
            logger.debug("Waiting for user credentials submission")
            return
        if not hcg_username or not hcg_password:
            logger.warning("Missing credentials - username or password not provided")
            st.error("Please enter both username and password.")
            return

        start_date, end_date = self.get_date_range()
        logger.info("User selected date range: %s to %s", start_date, end_date)
        self.visualize_steps(hcg_username, hcg_password, start_date, end_date)
