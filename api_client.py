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

    def request(
        self,
        method: str,
        endpoint: str,
        params=None,
        data=None,
        return_metadata=False
    ):
        """Send an authenticated request and handle API errors."""

        try:
            # Build API URL
            url = get_api_url(endpoint)

            # Include query parameters before OAuth signing
            request_url = str(
                httpx.URL(url).copy_merge_params(params or {})
            )

            # Generate OAuth 1.0 HMAC-SHA1 signature
            signed_url, headers, _ = self.auth_client.sign(
                request_url,
                http_method=method.upper(),
                body=None,
                headers={},
            )

            # Send HTTP request
            with httpx.Client(timeout=self.timeout) as client:
                response = client.request(
                    method=method.upper(),
                    url=signed_url,
                    headers=headers,
                    json=data,
                )

            # Handle unsuccessful HTTP responses
            if response.is_error:
                self.handle_http_error(response)

            # Parse JSON response
            try:
                result = response.json()

            except ValueError as exc:
                raise WooCommerceAPIError(
                    "Invalid API response: "
                    "WooCommerce returned invalid JSON."
                ) from exc

            # Validate response structure
            if not isinstance(result, (list, dict)):
                raise WooCommerceAPIError(
                    "Invalid API response: "
                    "Expected a JSON list or dictionary."
                )

            # Return pagination metadata when requested
            if return_metadata:
                try:
                    total = int(response.headers.get("X-WP-Total", 0))
                    total_pages = int(
                        response.headers.get("X-WP-TotalPages", 0)
                    )
                except (TypeError, ValueError) as exc:
                    raise WooCommerceAPIError(
                        "Invalid pagination metadata received from WooCommerce."
                    ) from exc

                return {
                    "data": result,
                    "total": total,
                    "total_pages": total_pages
                }

            # Return normal response for existing CLI functions
            return result

        except httpx.TimeoutException as exc:
            raise WooCommerceAPIError(
                f"Network timeout: WooCommerce did not respond "
                f"within {self.timeout} seconds."
            ) from exc

        except httpx.ConnectError as exc:
            raise WooCommerceAPIError(
                "API connection failed. Check your store URL "
                "and ensure WordPress is running."
            ) from exc

        except httpx.InvalidURL as exc:
            raise WooCommerceAPIError(
                "Incorrect store URL. Check WC_STORE_URL "
                "in your .env file."
            ) from exc

        except httpx.RequestError as exc:
            raise WooCommerceAPIError(
                f"Network request failed: {type(exc).__name__}."
            ) from exc

    @staticmethod
    def handle_http_error(response):
        """Convert HTTP errors into readable WooCommerce errors."""

        status_code = response.status_code

        error_messages = {
            400: "Bad request. Check the request parameters.",
            401: "Authentication failed. Check your API credentials.",
            403: "Access denied. Check your API key permissions.",
            404: "API endpoint not found. Check the store URL.",
            405: "HTTP method not allowed.",
            408: "Request timeout.",
            429: "Too many API requests. Try again later.",
            500: "Internal server error on the WordPress server.",
            502: "Bad gateway. The server is unavailable.",
            503: "WooCommerce service is unavailable.",
            504: "Gateway timeout. The server took too long to respond.",
        }

        message = error_messages.get(
            status_code,
            f"WooCommerce returned HTTP {status_code}.",
        )

        # Extract WooCommerce error details when available
        try:
            error_data = response.json()

            if isinstance(error_data, dict):
                api_message = error_data.get("message")

                if api_message:
                    message += f"\nAPI details: {api_message}"

        except ValueError:
            pass

        raise WooCommerceAPIError(message)


def create_order(
    client: WooCommerceClient,
    product_id: int,
    quantity: int,
    status: str,
) -> dict:
    """Create a WooCommerce order."""

    allowed_statuses = {
        "processing",
        "completed",
        "pending",
        "on-hold",
    }

    if status not in allowed_statuses:
        raise ValueError(f"Invalid order status: {status}")

    if product_id <= 0 or quantity <= 0:
        raise ValueError("Product ID and quantity must be positive.")

    order_data = {
        "status": status,
        "currency": "INR",
        "payment_method": "cod",
        "payment_method_title": "Cash on delivery",
        "set_paid": False,
        "billing": {
            "first_name": "Test",
            "last_name": "Customer",
            "email": "test@example.com",
        },
        "line_items": [
            {
                "product_id": product_id,
                "quantity": quantity,
            }
        ],
    }

    response = client.request(
        method="POST",
        endpoint="orders",
        data=order_data,
    )

    if not isinstance(response, dict) or "id" not in response:
        raise WooCommerceAPIError(
            "Invalid response while creating WooCommerce order."
        )

    return response


def create_test_orders(client: WooCommerceClient) -> list:
    """Create five test orders with different statuses."""

    statuses = [
        "processing",
        "completed",
        "pending",
        "on-hold",
        "processing",
    ]

    created_orders = []

    for status in statuses:
        order = create_order(
            client=client,
            product_id=387,
            quantity=1,
            status=status,
        )

        created_orders.append(order)

        print("\nOrder created successfully!")
        print(f"Order ID       : {order.get('id')}")
        print(f"Order Number   : {order.get('number')}")
        print("Customer       : Test Customer")
        print("Email          : test@example.com")
        print(f"Status         : {order.get('status')}")
        print(f"Currency       : {order.get('currency')}")
        print(f"Total          : {order.get('total')}")
        print(
            f"Payment Method : "
            f"{order.get('payment_method_title')}"
        )

    print(f"\nTotal orders created: {len(created_orders)}")

    return created_orders
