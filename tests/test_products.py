import pytest

from products import (
    get_products,
    search_products_by_name,
    search_products_by_sku,
)
from api_client import WooCommerceAPIError


class MockWooCommerceClient:
    """Mock client to test product operations without API requests."""

    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def request(self, method, endpoint, params=None, data=None):
        self.calls.append({
            "method": method,
            "endpoint": endpoint,
            "params": params,
        })

        if not self.responses:
            raise AssertionError("No mock response available.")

        return self.responses.pop(0)


def test_get_products_with_pagination():
    client = MockWooCommerceClient([
        [{"id": 1}, {"id": 2}],
        [{"id": 3}],
    ])

    result = get_products(client, per_page=2)

    assert len(result) == 3
    assert [product["id"] for product in result] == [1, 2, 3]
    assert len(client.calls) == 2
    assert client.calls[0]["params"]["page"] == 1
    assert client.calls[1]["params"]["page"] == 2
    assert client.calls[0]["params"]["status"] == "publish"


def test_get_products_returns_empty_list():
    client = MockWooCommerceClient([[]])

    result = get_products(client)

    assert result == []
    assert len(client.calls) == 1


def test_get_products_rejects_invalid_response():
    client = MockWooCommerceClient([
        {"message": "Invalid response"}
    ])

    with pytest.raises(WooCommerceAPIError):
        get_products(client)


def test_search_products_by_name():
    client = MockWooCommerceClient([
        [{"id": 1, "name": "Python Automation Scripts Bundle"}]
    ])

    result = search_products_by_name(
        client,
        "  Python Automation  "
    )

    assert len(result) == 1
    assert result[0]["name"] == "Python Automation Scripts Bundle"
    assert client.calls[0]["params"]["search"] == "Python Automation"


def test_search_products_by_name_rejects_empty_input():
    client = MockWooCommerceClient([])

    with pytest.raises(ValueError, match="Product name cannot be empty"):
        search_products_by_name(client, "   ")

    assert client.calls == []


def test_search_products_by_sku():
    client = MockWooCommerceClient([
        [{"id": 2, "sku": "PY-AUTO-001"}]
    ])

    result = search_products_by_sku(
        client,
        "  PY-AUTO-001  "
    )

    assert len(result) == 1
    assert result[0]["sku"] == "PY-AUTO-001"
    assert client.calls[0]["params"]["sku"] == "PY-AUTO-001"


def test_search_products_by_sku_rejects_empty_input():
    client = MockWooCommerceClient([])

    with pytest.raises(ValueError, match="Product SKU cannot be empty"):
        search_products_by_sku(client, "   ")

    assert client.calls == []


def test_search_products_rejects_invalid_response():
    client = MockWooCommerceClient([
        {"message": "Invalid response"}
    ])

    with pytest.raises(WooCommerceAPIError):
        search_products_by_name(client, "Python")

    client = MockWooCommerceClient([
        {"message": "Invalid response"}
    ])

    with pytest.raises(WooCommerceAPIError):
        search_products_by_sku(client, "PY-AUTO-001")
