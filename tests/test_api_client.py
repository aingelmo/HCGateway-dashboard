"""Tests for HCGateway API client functionality."""

from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests

from hcgateway_dashboard.api_client import HCGatewayClient, TokenManager


class TestTokenManager:
    """Test cases for TokenManager class."""

    def test_init(self) -> None:
        """Test TokenManager initialization."""
        manager = TokenManager()
        assert manager.access_token is None
        assert manager.refresh_token is None

    def test_is_token_expired_no_expiry(self) -> None:
        """Test token expiry check when no expiry is set."""
        manager = TokenManager()
        assert manager.is_token_expired() is True

    def test_is_token_expired_valid_token(self) -> None:
        """Test token expiry check with valid token."""
        manager = TokenManager()
        future_expiry = (datetime.now(UTC) + timedelta(hours=1)).isoformat()
        manager.update_tokens({"expiry": future_expiry})
        assert manager.is_token_expired() is False

    def test_is_token_expired_expired_token(self) -> None:
        """Test token expiry check with expired token."""
        manager = TokenManager()
        past_expiry = (datetime.now(UTC) - timedelta(minutes=1)).isoformat()
        manager.update_tokens({"expiry": past_expiry})
        assert manager.is_token_expired() is True

    def test_is_token_expired_margin(self) -> None:
        """Test token expiry check within expiry margin."""
        manager = TokenManager()
        # Token expires in 2 minutes (within 5-minute margin)
        near_expiry = (datetime.now(UTC) + timedelta(minutes=2)).isoformat()
        manager.update_tokens({"expiry": near_expiry})
        assert manager.is_token_expired() is True

    def test_update_tokens(self, mock_token_response: dict[str, Any]) -> None:
        """Test token update from API response."""
        manager = TokenManager()
        manager.update_tokens(mock_token_response)

        assert manager.access_token == mock_token_response["token"]
        assert manager.refresh_token == mock_token_response["refresh"]


class TestHCGatewayClient:
    """Test cases for HCGatewayClient class."""

    def test_init(self) -> None:
        """Test HCGatewayClient initialization."""
        client = HCGatewayClient()
        assert client._token_manager is not None
        assert client.BASE_URL == "https://api.hcgateway.shuchir.dev/api/v2"

    @patch("hcgateway_dashboard.api_client.requests.post")
    def test_get_access_token_success(
        self,
        mock_post: MagicMock,
        mock_requests_response: MagicMock,
        mock_token_response: dict[str, Any],
    ) -> None:
        """Test successful access token retrieval."""
        mock_requests_response.json.return_value = mock_token_response
        mock_post.return_value = mock_requests_response

        client = HCGatewayClient()
        result = client._get_access_token("test_user", "test_pass")

        assert result == mock_token_response
        mock_post.assert_called_once()

        # Check the request was made correctly
        call_args = mock_post.call_args
        assert call_args[1]["json"]["username"] == "test_user"
        assert call_args[1]["json"]["password"] == "test_pass"

    @patch("hcgateway_dashboard.api_client.requests.post")
    def test_get_access_token_failure(self, mock_post: MagicMock) -> None:
        """Test access token retrieval failure."""
        mock_post.side_effect = requests.RequestException("Connection failed")

        client = HCGatewayClient()

        with pytest.raises(requests.RequestException):
            client._get_access_token("test_user", "test_pass")

    @patch("hcgateway_dashboard.api_client.requests.post")
    def test_refresh_access_token_success(
        self,
        mock_post: MagicMock,
        mock_requests_response: MagicMock,
        mock_token_response: dict[str, Any],
    ) -> None:
        """Test successful token refresh."""
        mock_requests_response.json.return_value = mock_token_response
        mock_post.return_value = mock_requests_response

        client = HCGatewayClient()
        result = client._refresh_access_token("test_refresh_token")

        assert result == mock_token_response
        mock_post.assert_called_once()

    @patch("hcgateway_dashboard.api_client.requests.post")
    def test_refresh_access_token_failure(self, mock_post: MagicMock) -> None:
        """Test token refresh failure."""
        mock_post.side_effect = requests.RequestException("Refresh failed")

        client = HCGatewayClient()

        with pytest.raises(requests.RequestException):
            client._refresh_access_token("invalid_refresh_token")

    @patch.object(HCGatewayClient, "_get_access_token")
    def test_ensure_valid_token_no_token(
        self,
        mock_get_token: MagicMock,
        mock_token_response: dict[str, Any],
    ) -> None:
        """Test ensuring valid token when no token exists."""
        mock_get_token.return_value = mock_token_response

        client = HCGatewayClient()
        client._ensure_valid_token("test_user", "test_pass")

        mock_get_token.assert_called_once_with("test_user", "test_pass")
        assert client._token_manager.access_token == mock_token_response["token"]

    @patch.object(HCGatewayClient, "_refresh_access_token")
    @patch.object(HCGatewayClient, "_get_access_token")
    def test_ensure_valid_token_refresh_success(
        self,
        mock_get_token: MagicMock,
        mock_refresh_token: MagicMock,
        expired_token_response: dict[str, Any],
        mock_token_response: dict[str, Any],
    ) -> None:
        """Test ensuring valid token with successful refresh."""
        # Set up expired token
        client = HCGatewayClient()
        client._token_manager.update_tokens(expired_token_response)

        # Mock successful refresh
        mock_refresh_token.return_value = mock_token_response

        client._ensure_valid_token("test_user", "test_pass")

        mock_refresh_token.assert_called_once()
        mock_get_token.assert_not_called()
        assert client._token_manager.access_token == mock_token_response["token"]

    @patch.object(HCGatewayClient, "_refresh_access_token")
    @patch.object(HCGatewayClient, "_get_access_token")
    def test_ensure_valid_token_refresh_failure_fallback(
        self,
        mock_get_token: MagicMock,
        mock_refresh_token: MagicMock,
        expired_token_response: dict[str, Any],
        mock_token_response: dict[str, Any],
    ) -> None:
        """Test ensuring valid token with refresh failure and fallback to full auth."""
        # Set up expired token
        client = HCGatewayClient()
        client._token_manager.update_tokens(expired_token_response)

        # Mock refresh failure and successful full auth
        mock_refresh_token.side_effect = requests.RequestException("Refresh failed")
        mock_get_token.return_value = mock_token_response

        client._ensure_valid_token("test_user", "test_pass")

        mock_refresh_token.assert_called_once()
        mock_get_token.assert_called_once_with("test_user", "test_pass")
        assert client._token_manager.access_token == mock_token_response["token"]

    @patch("hcgateway_dashboard.api_client.requests.post")
    @patch.object(HCGatewayClient, "_ensure_valid_token")
    def test_fetch_data_success(
        self,
        mock_ensure_token: MagicMock,
        mock_post: MagicMock,
        mock_requests_response: MagicMock,
        mock_steps_data: list[dict[str, Any]],
    ) -> None:
        """Test successful data fetching."""
        mock_requests_response.json.return_value = mock_steps_data
        mock_post.return_value = mock_requests_response

        client = HCGatewayClient()
        client._token_manager.update_tokens({"token": "test_token"})

        result = client.fetch_data("steps", {}, "test_user", "test_pass")

        assert result == mock_steps_data
        mock_ensure_token.assert_called_once_with("test_user", "test_pass")
        mock_post.assert_called_once()

    @patch("hcgateway_dashboard.api_client.requests.post")
    @patch.object(HCGatewayClient, "_ensure_valid_token")
    def test_fetch_data_failure(
        self,
        mock_ensure_token: MagicMock,
        mock_post: MagicMock,
    ) -> None:
        """Test data fetching failure."""
        mock_post.side_effect = requests.RequestException("API error")

        client = HCGatewayClient()

        with pytest.raises(requests.RequestException):
            client.fetch_data("steps", {}, "test_user", "test_pass")

        mock_ensure_token.assert_called_once()


class TestIntegration:
    """Integration tests for the API client."""

    @pytest.mark.skipif(
        not all(
            [
                pytest.importorskip("os").getenv("TEST_HCGATEWAY_USERNAME"),
                pytest.importorskip("os").getenv("TEST_HCGATEWAY_PASSWORD"),
            ]
        ),
        reason="Integration test credentials not provided",
    )
    def test_real_api_integration(self, test_credentials: tuple[str, str]) -> None:
        """Test actual API integration (requires real credentials)."""
        username, password = test_credentials

        client = HCGatewayClient()

        # Test authentication and data fetching
        result = client.fetch_data("steps", {}, username, password)

        assert isinstance(result, list)
        # Don't assert specific content as it depends on real data
