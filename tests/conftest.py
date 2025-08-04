"""Test configuration and fixtures for HCGateway Dashboard tests."""

import os
from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_token_response() -> dict[str, Any]:
    """Create a mock token response from the API."""
    return {
        "token": "test_access_token_123",
        "refresh": "test_refresh_token_456",
        "expiry": (datetime.now(UTC) + timedelta(hours=1)).isoformat(),
    }


@pytest.fixture
def expired_token_response() -> dict[str, Any]:
    """Create a mock expired token response."""
    return {
        "token": "expired_token",
        "refresh": "expired_refresh",
        "expiry": (datetime.now(UTC) - timedelta(minutes=10)).isoformat(),
    }


@pytest.fixture
def mock_steps_data() -> list[dict[str, Any]]:
    """Create mock steps data for testing."""
    return [
        {
            "_id": "test_id_1",
            "app": "TestApp",
            "data": {"count": 5000},
            "end": "2024-08-01T23:59:59Z",
            "id": "step_1",
            "start": "2024-08-01T00:00:00Z",
        },
        {
            "_id": "test_id_2",
            "app": "TestApp",
            "data": {"count": 7500},
            "end": "2024-08-02T23:59:59Z",
            "id": "step_2",
            "start": "2024-08-02T00:00:00Z",
        },
    ]


@pytest.fixture
def test_credentials() -> tuple[str, str]:
    """Get test credentials from environment or use defaults."""
    username = os.getenv("TEST_HCGATEWAY_USERNAME", "test_user")
    password = os.getenv("TEST_HCGATEWAY_PASSWORD", "test_pass")
    return username, password


@pytest.fixture
def mock_requests_response() -> MagicMock:
    """Create a mock requests response object."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    return mock_response
