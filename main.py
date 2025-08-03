import logging
import os

import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


def main():
    logger.info("Starting HCGateway login script.")

    hcg_username = os.getenv("HCGATEWAY_USERNAME")
    hcg_password = os.getenv("HCGATEWAY_PASSWORD")

    if not hcg_username or not hcg_password:
        logger.error(
            "Missing HCGATEWAY_USERNAME or HCGATEWAY_PASSWORD environment variables."
        )
        raise ValueError(
            "Missing HCGATEWAY_USERNAME or HCGATEWAY_PASSWORD environment variables."
        )

    url = "https://api.hcgateway.shuchir.dev/api/v2/login"
    headers = {"Content-Type": "application/json"}
    data = {"username": hcg_username, "password": hcg_password}

    try:
        logger.debug(f"Sending POST request to {url} with username {hcg_username}")
        response = requests.post(url, headers=headers, json=data)
        logger.info(f"Response status code: {response.status_code}")
        response.raise_for_status()

        resp_json = response.json()
        expires = resp_json.get("expiry")
        access_token = resp_json.get("token")
        refresh_token = resp_json.get("refresh")

        logger.debug(f"Response JSON: {resp_json}")
        logger.info(f"Token expires: {expires}")
        logger.info(f"Access token: {access_token}")
        logger.info(f"Refresh token: {refresh_token}")

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()
