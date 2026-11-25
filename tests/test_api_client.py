import httpx
import pytest

import api_client
from api_client import WooCommerceAPIError, WooCommerceClient


def create_test_client(
    monkeypatch,
    status_code=200,
    response_json=None,
    response_content=None,
    request_error=None,
):
    """Create a WooCommerce client with a mocked HTTP connection."""

    captured = {}

    # Prevent tests from depending on real WooCommerce credentials.
    monkeypatch.setattr(api_client, "validate_config", lambda: None)
    monkeypatch.setattr(api_client, "WC_CONSUMER_KEY", "ck_test")
    monkeypatch.setattr(api_client, "WC_CONSUMER_SECRET", "cs_test")
    monkeypatch.setattr(api_client, "WC_TIMEOUT", 5)
    monkeypatch.setattr(
        api_client,
        "get_api_url",
        lambda endpoint: (
            f"https://shop.example/wp-json/wc/v3/{endpoint.lstrip('/')}"
        ),
    )

    class MockHTTPClient:
        def __init__(self, timeout):
            captured["timeout"] = timeout

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

        def request(self, method, url, headers=None, json=None):
            captured["method"] = method
            captured["url"] = url
            captured["headers"] = headers
            captured["json"] = json

            request = httpx.Request(method, url)

            if request_error:
                raise request_error(request)

            if response_content is not None:
                return httpx.Response(
                    status_code,
                    content=response_content,
                    request=request,
                )

            return httpx.Response(
                status_code,
                json=response_json,
                request=request,
            )

    monkeypatch.setattr(api_client.httpx, "Client", MockHTTPClient)

    return WooCommerceClient(), captured


def test_request_returns_json_and_signs_oauth(monkeypatch):
    client, captured = create_test_client(
        monkeypatch,
        response_json=[{"id": 1, "name": "Test Product"}],
    )

    result = client.request(
        "GET",
        "products",
        params={"per_page": 5},
    )

    assert result[0]["id"] == 1
    assert captured["method"] == "GET"
    assert captured["timeout"] == 5

    signed_url = httpx.URL(captured["url"])

    assert signed_url.params["per_page"] == "5"
    assert signed_url.params["oauth_consumer_key"] == "ck_test"
    assert signed_url.params["oauth_signature"]


def test_request_sends_json_data(monkeypatch):
    client, captured = create_test_client(
        monkeypatch,
        response_json={"id": 100},
    )

    order_data = {
        "payment_method": "cod",
        "status": "pending",
    }

    result = client.request(
        "POST",
        "orders",
        data=order_data,
    )

    assert result["id"] == 100
    assert captured["method"] == "POST"
    assert captured["json"] == order_data


@pytest.mark.parametrize(
    ("status_code", "expected_message"),
    [
        (401, "Authentication failed"),
        (403, "Access denied"),
        (404, "API endpoint not found"),
        (500, "WooCommerce returned HTTP 500"),
    ],
)
def test_http_errors_are_handled(
    monkeypatch,
    status_code,
    expected_message,
):
    client, _ = create_test_client(
        monkeypatch,
        status_code=status_code,
        response_json={"message": "API error"},
    )

    with pytest.raises(WooCommerceAPIError, match=expected_message):
        client.request("GET", "products")


def test_timeout_error_is_handled(monkeypatch):
    client, _ = create_test_client(
        monkeypatch,
        request_error=lambda request: httpx.TimeoutException(
            "Connection timed out",
            request=request,
        ),
    )

    with pytest.raises(WooCommerceAPIError, match="Request timed out"):
        client.request("GET", "products")


def test_connection_error_is_handled(monkeypatch):
    client, _ = create_test_client(
        monkeypatch,
        request_error=lambda request: httpx.ConnectError(
            "Connection failed",
            request=request,
        ),
    )

    with pytest.raises(WooCommerceAPIError, match="Could not connect"):
        client.request("GET", "products")


def test_invalid_json_response_is_handled(monkeypatch):
    client, _ = create_test_client(
        monkeypatch,
        response_content=b"not valid JSON",
    )

    with pytest.raises(WooCommerceAPIError, match="invalid JSON"):
        client.request("GET", "products")
