from decimal import Decimal, InvalidOperation

from store_api_client import (
    WooCommerceStoreClient,
    StoreAPIError,
)


def get_cart(client: WooCommerceStoreClient) -> dict:
    """Retrieve the current shopping cart."""

    response = client.request("GET", "cart")

    if not isinstance(response, dict):
        raise StoreAPIError("Invalid cart response.")

    return response


def add_to_cart(
    client: WooCommerceStoreClient,
    product_id: int,
    quantity: int = 1,
) -> dict:
    """Add a product to the shopping cart."""

    if product_id <= 0:
        raise ValueError("Product ID must be positive.")

    if quantity <= 0:
        raise ValueError("Quantity must be positive.")

    return client.request(
        "POST",
        "cart/add-item",
        data={
            "id": product_id,
            "quantity": quantity,
        },
    )


def update_cart_item(
    client: WooCommerceStoreClient,
    item_key: str,
    quantity: int,
) -> dict:
    """Update the quantity of a cart item."""

    if not item_key.strip():
        raise ValueError("Cart item key cannot be empty.")

    if quantity <= 0:
        raise ValueError("Quantity must be positive.")

    return client.request(
        "POST",
        "cart/update-item",
        data={
            "key": item_key,
            "quantity": quantity,
        },
    )


def remove_from_cart(
    client: WooCommerceStoreClient,
    item_key: str,
) -> dict:
    """Remove an item from the shopping cart."""

    if not item_key.strip():
        raise ValueError("Cart item key cannot be empty.")

    return client.request(
        "POST",
        "cart/remove-item",
        data={
            "key": item_key,
        },
    )


def apply_coupon(
    client: WooCommerceStoreClient,
    coupon_code: str,
) -> dict:
    """Apply a discount coupon to the shopping cart."""

    if not coupon_code.strip():
        raise ValueError("Coupon code cannot be empty.")

    return client.request(
        "POST",
        "cart/apply-coupon",
        data={
            "code": coupon_code.strip(),
        },
    )


def format_amount(amount, currency_data: dict) -> str:
    """Format WooCommerce minor-unit amounts."""

    try:
        minor_unit = currency_data.get("currency_minor_unit", 2)
        value = Decimal(str(amount)) / (Decimal(10) ** minor_unit)

        symbol = currency_data.get("currency_symbol", "")
        return f"{symbol}{value:,.{minor_unit}f}"

    except (InvalidOperation, TypeError, ValueError):
        return str(amount)


def display_cart(cart: dict) -> None:
    """Display shopping cart information."""

    items = cart.get("items", [])
    totals = cart.get("totals", {})

    print("\n" + "=" * 65)
    print("                 NOREVIA SHOPPING CART")
    print("=" * 65)

    if not items:
        print("\nYour shopping cart is empty.")
        return

    currency_data = {
        "currency_symbol": totals.get("currency_symbol", "₹"),
        "currency_minor_unit": totals.get("currency_minor_unit", 2),
    }

    for item in items:
        prices = item.get("prices") or {}

        print(f"\nProduct  : {item.get('name', 'N/A')}")
        print(f"Quantity : {item.get('quantity', 0)}")
        print(
            "Price    : "
            f"{format_amount(prices.get('price', '0'), currency_data)}"
        )
        print(f"Item Key : {item.get('key', 'N/A')}")
        print("-" * 65)

    print(f"\nTotal Items : {cart.get('items_count', 0)}")
    print(
        "Subtotal    : "
        f"{format_amount(totals.get('total_items', '0'), currency_data)}"
    )
    print(
        "Discount    : "
        f"{format_amount(totals.get('total_discount', '0'), currency_data)}"
    )
    print(
        "Total       : "
        f"{format_amount(totals.get('total_price', '0'), currency_data)}"
    )
    print("=" * 65)
