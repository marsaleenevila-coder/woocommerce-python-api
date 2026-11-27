
import os
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv


# Load environment variables from the project root .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


# WooCommerce configuration
WC_STORE_URL = os.getenv("WC_STORE_URL", "").strip().rstrip("/")
WC_CONSUMER_KEY = os.getenv("WC_CONSUMER_KEY", "").strip()
WC_CONSUMER_SECRET = os.getenv("WC_CONSUMER_SECRET", "").strip()
WC_API_VERSION = os.getenv("WC_API_VERSION", "wc/v3").strip()
WC_TIMEOUT = float(os.getenv("WC_TIMEOUT", "30"))


def validate_config():
    """Validate the required WooCommerce configuration."""

    required_settings = {
        "WC_STORE_URL": WC_STORE_URL,
        "WC_CONSUMER_KEY": WC_CONSUMER_KEY,
        "WC_CONSUMER_SECRET": WC_CONSUMER_SECRET,
    }

    missing_settings = [
        name
        for name, value in required_settings.items()
        if not value
    ]

    if missing_settings:
        raise ValueError(
            "Missing required environment variables: "
            + ", ".join(missing_settings)
        )

    # Validate store URL
    try:
        parsed_url = urlsplit(WC_STORE_URL)

        if (
            parsed_url.scheme not in ("http", "https")
            or not parsed_url.hostname
            or parsed_url.username
            or parsed_url.password
            or parsed_url.query
            or parsed_url.fragment
        ):
            raise ValueError

        # Validate the port if provided
        _ = parsed_url.port

    except ValueError:
        raise ValueError(
            "Invalid WC_STORE_URL. Enter a valid URL "
            "starting with http:// or https://."
        )

    # Validate timeout
    if WC_TIMEOUT <= 0:
        raise ValueError(
            "WC_TIMEOUT must be greater than zero."
        )

    # Validate API version
    if not WC_API_VERSION:
        raise ValueError(
            "WC_API_VERSION cannot be empty."
        )


def get_api_url(endpoint: str) -> str:
    """Build the WooCommerce REST API endpoint URL."""

    return (
        f"{WC_STORE_URL}/wp-json/{WC_API_VERSION}/"
        f"{endpoint.lstrip('/')}"
    )
