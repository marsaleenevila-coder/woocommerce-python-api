import httpx
from oauthlib.oauth1 import (
    Client,
    SIGNATURE_HMAC_SHA1,
    SIGNATURE_TYPE_QUERY,
)

from config import (
    WC_CONSUMER_KEY,
    WC_CONSUMER_SECRET,
    WC_TIMEOUT,
    get_api_url,
    validate_config,
)


class WooCommerceAPIError(Exception):
    """Custom exception for WooCommerce API errors."""


class WooCommerceClient:
    """HTTP client for communicating with WooCommerce REST API."""

    def __init__(self):
        validate_config()

        self.auth_client = Client(
            client_key=WC_CONSUMER_KEY,
            client_secret=WC_CONSUMER_SECRET,
            signature_method=SIGNATURE_HMAC_SHA1,
            signature_type=SIGNATURE_TYPE_QUERY,
        )

        self.timeout = WC_TIMEOUT

    def request(self, method: str, endpoint: str, params=None):
        """Send an authenticated request to WooCommerce."""

        url = get_api_url(endpoint)

        # Include query parameters before OAuth signing.
        request_url = str(
            httpx.URL(url).copy_merge_params(params or {})
        )

        # Generate OAuth 1.0 HMAC-SHA1 signature.
        signed_url, headers, _ = self.auth_client.sign(
            request_url,
            http_method=method.upper(),
            body=None,
            headers={},
        )

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.request(
                    method=method.upper(),
                    url=signed_url,
                    headers=headers,
                )

            response.raise_for_status()

            try:
                return response.json()
            except ValueError as exc:
                raise WooCommerceAPIError(
                    "WooCommerce returned an invalid JSON response."
                ) from exc

        except httpx.TimeoutException as exc:
            raise WooCommerceAPIError(
                "Request timed out while connecting to WooCommerce."
            ) from exc

        except httpx.ConnectError as exc:
            raise WooCommerceAPIError(
                "Could not connect to WooCommerce. Check the store URL."
            ) from exc

        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code

            error_messages = {
                401: "Authentication failed. Check your API credentials.",
                403: "Access denied. Check API key permissions.",
                404: "API endpoint not found. Check the store URL.",
            }

            message = error_messages.get(
                status_code,
                f"WooCommerce returned HTTP {status_code}.",
            )

            raise WooCommerceAPIError(message) from exc

        except httpx.RequestError as exc:
            raise WooCommerceAPIError(
                f"An HTTP request error occurred: {exc}"
            ) from exc
