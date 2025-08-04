"""API client for HCGateway authentication and data fetching."""

import logging
from datetime import UTC, datetime
from typing import Any

import requests

from hcgateway_dashboard.config import TOKEN_EXPIRY_MARGIN_SECONDS


logger = logging.getLogger("hcgateway.api_client")


class TokenManager:
    """Manages authentication tokens for HCGateway API."""

    def __init__(self) -> None:
        """Initialize token manager with empty token data."""
        self._token_data: dict[str, str | None] = {
            "access_token": None,
            "refresh_token": None,
            "expiry": None,
        }

    @property
    def access_token(self) -> str | None:
        """Get current access token."""
        return self._token_data["access_token"]

    @property
    def refresh_token(self) -> str | None:
        """Get current refresh token."""
        return self._token_data["refresh_token"]

    def is_token_expired(self) -> bool:
        """Check if the current token is expired or about to expire (within 5 minutes)."""
        expiry_str = self._token_data.get("expiry")
        if not expiry_str:
            return True
        expiry = datetime.fromisoformat(expiry_str).astimezone(UTC)
        now = datetime.now(UTC)
        return (expiry - now).total_seconds() < TOKEN_EXPIRY_MARGIN_SECONDS

    def update_tokens(self, token_response: dict[str, Any]) -> None:
        """Update stored tokens from API response."""
        self._token_data["access_token"] = token_response.get("token")
        self._token_data["refresh_token"] = token_response.get("refresh")
        expiry_str = token_response.get("expiry")
        self._token_data["expiry"] = expiry_str if expiry_str else None


class HCGatewayClient:
    """Client for HCGateway API operations."""

    BASE_URL = "https://api.hcgateway.shuchir.dev/api/v2"
    REQUEST_TIMEOUT = 10

    def __init__(self) -> None:
        """Initialize HCGateway API client."""
        self._token_manager = TokenManager()

    def _get_access_token(self, username: str, password: str) -> dict[str, Any]:
        """Authenticate and return the response JSON with tokens."""
        url = f"{self.BASE_URL}/login"
        headers = {"Content-Type": "application/json"}
        data = {"username": username, "password": password}

        try:
            logger.debug("Sending POST request to %s with username %s", url, username)
            response = requests.post(url, headers=headers, json=data, timeout=self.REQUEST_TIMEOUT)
            logger.info("Response status code: %s", response.status_code)
            response.raise_for_status()
            resp_json = response.json()
            logger.debug("Response JSON: %s", resp_json)
            return resp_json
        except requests.RequestException:
            logger.exception("Authentication request failed")
            raise

    def _refresh_access_token(self, refresh_token: str) -> dict[str, Any]:
        """Refresh and return a new access token using the refresh token."""
        url = f"{self.BASE_URL}/refresh"
        headers = {"Content-Type": "application/json"}
        data = {"refresh": refresh_token}

        try:
            logger.debug("Sending POST request to %s with refresh token", url)
            response = requests.post(url, headers=headers, json=data, timeout=self.REQUEST_TIMEOUT)
            logger.info("Refresh response status code: %s", response.status_code)
            response.raise_for_status()
            resp_json = response.json()
            logger.debug("Refresh response JSON: %s", resp_json)
            return resp_json
        except requests.RequestException:
            logger.exception("Token refresh request failed")
            raise

    def _ensure_valid_token(self, username: str, password: str) -> None:
        """Ensure a valid access token is available, refreshing if needed."""
        if not self._token_manager.access_token or self._token_manager.is_token_expired():
            if self._token_manager.refresh_token:
                try:
                    resp = self._refresh_access_token(self._token_manager.refresh_token)
                    self._token_manager.update_tokens(resp)
                    return
                except requests.RequestException:
                    logger.warning("Token refresh failed, attempting full authentication")

            resp = self._get_access_token(username, password)
            self._token_manager.update_tokens(resp)

    def fetch_data(
        self,
        method: str,
        queries: dict[str, Any],
        username: str,
        password: str,
    ) -> dict[str, Any]:
        """Fetch data from the API using the specified method and queries."""
        self._ensure_valid_token(username, password)

        url = f"{self.BASE_URL}/fetch/{method}"
        headers = {
            "Authorization": f"Bearer {self._token_manager.access_token}",
            "Content-Type": "application/json",
        }
        data = {"queries": queries}

        try:
            logger.debug("Sending POST request to %s with queries %s", url, queries)
            response = requests.post(url, headers=headers, json=data, timeout=self.REQUEST_TIMEOUT)
            logger.info("Fetch response status code: %s", response.status_code)
            response.raise_for_status()
            resp_json = response.json()
            logger.debug("Fetch response JSON: %s", resp_json)
            return resp_json
        except requests.RequestException:
            logger.exception("Data fetch request failed")
            raise
