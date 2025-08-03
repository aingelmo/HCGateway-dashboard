"""Test data extraction from HCGateway API."""

import logging
import os

import pytest

from data_extractor import fetch_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_fetch_data_env() -> None:
    """Test fetch_data returns a list of dicts and does not expose tokens."""
    hcg_username = os.getenv("HCGATEWAY_USERNAME")
    hcg_password = os.getenv("HCGATEWAY_PASSWORD")
    if not hcg_username or not hcg_password:
        pytest.skip("Environment variables for credentials not set.")
    method = "steps"
    queries = {}
    result = fetch_data(method, queries, hcg_username, hcg_password)
    logger.info("DEBUG: fetch_data returned type: %s, value: %s", type(result), result)
    if not isinstance(result, list):
        msg = f"Result is not a list. Got {type(result)}: {result}"
        raise TypeError(msg)
    for item in result:
        if not isinstance(item, dict):
            msg = f"List item is not a dict. Got {type(item)}: {item}"
            raise TypeError(msg)
        if "token" in item:
            msg = "Result item should not expose tokens."
            raise AssertionError(msg)
