import httpx

from config import WC_STORE_URL, WC_TIMEOUT


class StoreAPIError(Exception):
    """Custom exception for WooCommerce Store API errors."""


class WooCommerceStoreClient:
    """Client for WooCommerce customer-facing Store API."""

    def __init__(self):
        if not WC_STORE_URL:
            raise ValueError("WC_STORE_URL is not configured.")

        self.base_url = (
            f"{WC_STORE_URL}/wp-json/wc/store/v1"
        )

        self.timeout = WC_TIMEOUT
        self.session = httpx.Client(timeout=self.timeout)

        self.cart_token = None
        self.nonce = None

    def request(self, method: str, endpoint: str, data=None):
        """Send a request to WooCommerce Store API."""

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        headers = {}

        if self.cart_token:
            headers["Cart-Token"] = self.cart_token

        if self.nonce:
            headers["Nonce"] = self.nonce

        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                json=data,
                headers=headers,
            )

            response.raise_for_status()

            self.cart_token = (
                response.headers.get("Cart-Token")
                or self.cart_token
            )

            self.nonce = (
                response.headers.get("Nonce")
                or self.nonce
            )

            return response.json()

        except httpx.TimeoutException as exc:
            raise StoreAPIError(
                "Store API request timed out."
            ) from exc

        except httpx.ConnectError as exc:
            raise StoreAPIError(
                "Could not connect to the WooCommerce Store API."
            ) from exc

        except httpx.HTTPStatusError as exc:
            try:
                error_data = exc.response.json()
                message = error_data.get(
                    "message",
                    f"HTTP {exc.response.status_code}"
                )
            except ValueError:
                message = f"HTTP {exc.response.status_code}"

            raise StoreAPIError(message) from exc

        except httpx.RequestError as exc:
            raise StoreAPIError(
                f"Store API request error: {exc}"
            ) from exc

        except ValueError as exc:
            raise StoreAPIError(
                "Store API returned invalid JSON."
            ) from exc

    def close(self):
        """Close the HTTP session."""

        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
