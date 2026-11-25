import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from the project root .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# WooCommerce configuration
WC_STORE_URL = os.getenv("WC_STORE_URL", "").rstrip("/")
WC_CONSUMER_KEY = os.getenv("WC_CONSUMER_KEY", "")
WC_CONSUMER_SECRET = os.getenv("WC_CONSUMER_SECRET", "")
WC_API_VERSION = os.getenv("WC_API_VERSION", "wc/v3")
WC_TIMEOUT = float(os.getenv("WC_TIMEOUT", "30"))


def validate_config():
    """Validate the required WooCommerce configuration."""

    required_settings = {
        "WC_STORE_URL": WC_STORE_URL,
        "WC_CONSUMER_KEY": WC_CONSUMER_KEY,
        "WC_CONSUMER_SECRET": WC_CONSUMER_SECRET,
    }

    missing_settings = [
        name for name, value in required_settings.items() if not value
    ]

    if missing_settings:
        raise ValueError(
            f"Missing required environment variables: "
            f"{', '.join(missing_settings)}"
        )

    if not WC_STORE_URL.startswith(("http://", "https://")):
        raise ValueError("WC_STORE_URL must start with http:// or https://")

    if WC_TIMEOUT <= 0:
        raise ValueError("WC_TIMEOUT must be greater than zero")

def get_api_url(endpoint: str) -> str:
    """Build the WooCommerce REST API endpoint URL."""

    return (
        f"{WC_STORE_URL}/wp-json/{WC_API_VERSION}/"
        f"{endpoint.lstrip('/')}"
    )
