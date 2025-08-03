"""Test data extraction from HCGateway API."""

import os

import pytest

from data_extractor import fetch_data


def test_fetch_data_env() -> None:
    """Test fetch_data returns a dict and does not expose tokens."""
    hcg_username = os.getenv("HCGATEWAY_USERNAME")
    hcg_password = os.getenv("HCGATEWAY_PASSWORD")
    if not hcg_username or not hcg_password:
        pytest.skip("Environment variables for credentials not set.")
    method = "steps"
    queries = {}
    result = fetch_data(method, queries, hcg_username, hcg_password)
    if not isinstance(result, dict):
        msg = "Result is not a dict."
        raise TypeError(msg)
    if "token" in result:
        msg = "Result should not expose tokens."
        raise AssertionError(msg)
