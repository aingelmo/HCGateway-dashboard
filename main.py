"""Main script for HCGateway login functionality."""

import argparse
import json
import logging
import os
from datetime import UTC, datetime

import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

token_data = {
    "access_token": None,
    "refresh_token": None,
    "expiry": None,
}

TOKEN_EXPIRY_MARGIN_SECONDS = 300  # 5 minutes


def get_access_token(hcg_username: str, hcg_password: str) -> dict:
    """Authenticate and return the response JSON with tokens."""
    url = "https://api.hcgateway.shuchir.dev/api/v2/login"
    headers = {"Content-Type": "application/json"}
    data = {"username": hcg_username, "password": hcg_password}
    try:
        logger.debug("Sending POST request to %s with username %s", url, hcg_username)
        response = requests.post(url, headers=headers, json=data, timeout=10)
        logger.info("Response status code: %s", response.status_code)
        response.raise_for_status()
        resp_json = response.json()
        logger.debug("Response JSON: %s", resp_json)
    except requests.RequestException:
        logger.exception("Request failed")
        raise
    else:
        return resp_json


def refresh_access_token(refresh_token: str) -> dict:
    """Refresh and return a new access token using the refresh token."""
    url = "https://api.hcgateway.shuchir.dev/api/v2/refresh"
    headers = {"Content-Type": "application/json"}
    data = {"refresh": refresh_token}
    try:
        logger.debug("Sending POST request to %s with refresh token", url)
        response = requests.post(url, headers=headers, json=data, timeout=10)
        logger.info("Refresh response status code: %s", response.status_code)
        response.raise_for_status()
        resp_json = response.json()
        logger.debug("Refresh response JSON: %s", resp_json)
    except requests.RequestException:
        logger.exception("Refresh request failed")
        raise
    else:
        return resp_json


def ensure_valid_token(hcg_username: str, hcg_password: str) -> None:
    """Ensure a valid access token is available, refreshing if needed."""
    if not token_data["access_token"] or is_token_expired():
        if token_data["refresh_token"]:
            resp = refresh_access_token(token_data["refresh_token"])
        else:
            resp = get_access_token(hcg_username, hcg_password)
        token_data["access_token"] = resp.get("token")
        token_data["refresh_token"] = resp.get("refresh")
        expiry_str = resp.get("expiry")
        if expiry_str:
            # Store expiry as ISO string for type consistency
            token_data["expiry"] = expiry_str
        else:
            token_data["expiry"] = None


def is_token_expired() -> bool:
    """Check if the current token is expired or about to expire (within 5 minutes)."""
    expiry_str = token_data.get("expiry")
    if not expiry_str:
        return True
    expiry = datetime.fromisoformat(expiry_str).astimezone(UTC)
    now = datetime.now(UTC)
    return (expiry - now).total_seconds() < TOKEN_EXPIRY_MARGIN_SECONDS


def fetch_data(
    method: str,
    queries: dict,
    hcg_username: str,
    hcg_password: str,
) -> dict:
    """Fetch data from the API using the specified method and queries."""
    ensure_valid_token(hcg_username, hcg_password)
    url = f"https://api.hcgateway.shuchir.dev/api/v2/fetch/{method}"
    headers = {
        "Authorization": f"Bearer {token_data['access_token']}",
        "Content-Type": "application/json",
    }
    data = {"queries": queries}
    try:
        logger.debug("Sending POST request to %s with queries %s", url, queries)
        response = requests.post(url, headers=headers, json=data, timeout=10)
        logger.info("Fetch response status code: %s", response.status_code)
        response.raise_for_status()
        resp_json = response.json()
        logger.debug("Fetch response JSON: %s", resp_json)
    except requests.RequestException:
        logger.exception("Fetch request failed")
        raise
    else:
        return resp_json


def main() -> None:
    """Entry point for the HCGateway login script."""
    parser = argparse.ArgumentParser(description="Fetch data from HCGateway API.")
    parser.add_argument("method", type=str, help="API method to fetch (e.g., steps)")
    parser.add_argument(
        "--query",
        type=str,
        default="{}",
        help="MongoDB query as a JSON string (default: '{}')",
    )
    args = parser.parse_args()

    logger.info("Starting HCGateway login script.")

    hcg_username = os.getenv("HCGATEWAY_USERNAME")
    hcg_password = os.getenv("HCGATEWAY_PASSWORD")

    if not hcg_username or not hcg_password:
        msg = "Missing HCGATEWAY_USERNAME or HCGATEWAY_PASSWORD environment variables."
        logger.error(msg)
        raise OSError(msg)

    ensure_valid_token(hcg_username, hcg_password)
    logger.info("Current access token: %s", token_data["access_token"])

    try:
        queries = json.loads(args.query)
    except json.JSONDecodeError:
        logger.exception("Invalid JSON for --query")
        raise

    try:
        result = fetch_data(args.method, queries, hcg_username, hcg_password)
        logger.info("Fetched data for '%s': %s", args.method, result)
        logger.info("Fetched data output (JSON): %s", json.dumps(result, indent=2))
    except requests.RequestException:
        logger.exception("Failed to fetch '%s' data", args.method)


if __name__ == "__main__":
    main()
