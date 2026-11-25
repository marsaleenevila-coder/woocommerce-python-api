
from store_api_client import (
    WooCommerceStoreClient,
    StoreAPIError,
)


def get_checkout(
    client: WooCommerceStoreClient,
) -> dict:
    """Retrieve the current checkout information."""

    response = client.request("GET", "checkout")

    if not isinstance(response, dict):
        raise StoreAPIError("Invalid checkout response.")

    return response


def update_customer_addresses(
    client: WooCommerceStoreClient,
    billing_address: dict,
    shipping_address: dict | None = None,
) -> dict:
    """Update customer billing and shipping addresses."""

    if not isinstance(billing_address, dict) or not billing_address:
        raise ValueError("Billing address is required.")

    data = {
        "billing_address": billing_address,
    }

    if shipping_address is not None:
        if not isinstance(shipping_address, dict):
            raise ValueError("Shipping address must be a dictionary.")

        data["shipping_address"] = shipping_address

    return client.request(
        "POST",
        "cart/update-customer",
        data=data,
    )


def get_payment_methods(
    client: WooCommerceStoreClient,
) -> list:
    """Retrieve available payment methods from the cart."""

    cart = client.request("GET", "cart")
    methods = cart.get("payment_methods", [])

    if not isinstance(methods, list):
        raise StoreAPIError("Invalid payment methods response.")

    return methods


def set_payment_method(
    client: WooCommerceStoreClient,
    payment_method: str,
) -> dict:
    """Select a checkout payment method."""

    if not isinstance(payment_method, str) or not payment_method.strip():
        raise ValueError("Payment method cannot be empty.")

    payment_method = payment_method.strip()
    available_methods = get_payment_methods(client)

    if payment_method not in available_methods:
        raise ValueError(
            f"Payment method '{payment_method}' is unavailable. "
            f"Available methods: {available_methods}"
        )

    return client.request(
        "PUT",
        "checkout",
        data={"payment_method": payment_method},
    )


def validate_checkout(
    checkout: dict,
    payment_method: str,
    available_methods: list,
) -> None:
    """Validate checkout information before order submission."""

    if not isinstance(checkout, dict):
        raise ValueError("Invalid checkout information.")

    billing = checkout.get("billing_address") or {}

    if not isinstance(billing, dict):
        raise ValueError("Invalid billing address.")

    required_fields = [
        "first_name",
        "last_name",
        "address_1",
        "city",
        "state",
        "postcode",
        "country",
        "email",
        "phone",
    ]

    missing_fields = [
        field
        for field in required_fields
        if not str(billing.get(field, "")).strip()
    ]

    if missing_fields:
        raise ValueError(
            "Missing required billing fields: "
            + ", ".join(missing_fields)
        )

    if not isinstance(available_methods, list):
        raise ValueError("Invalid payment methods list.")

    if not isinstance(payment_method, str) or not payment_method.strip():
        raise ValueError("Payment method cannot be empty.")

    if payment_method not in available_methods:
        raise ValueError(
            f"Payment method '{payment_method}' is unavailable. "
            f"Available methods: {available_methods}"
        )


def submit_checkout(
    client: WooCommerceStoreClient,
    billing_address: dict,
    payment_method: str,
    shipping_address: dict | None = None,
    customer_note: str | None = None,
    payment_data: list | None = None,
    expected_total: str | None = None,
) -> dict:
    """
    Submit checkout and create a WooCommerce order.

    WARNING:
    Calling this function creates an actual WooCommerce order
    and may initiate payment processing.
    """

    available_methods = get_payment_methods(client)

    checkout_data = {
        "billing_address": billing_address,
    }

    validate_checkout(
        checkout_data,
        payment_method,
        available_methods,
    )

    if shipping_address is None:
        shipping_address = billing_address

    if not isinstance(shipping_address, dict) or not shipping_address:
        raise ValueError("Invalid shipping address.")

    if customer_note is not None:
        if not isinstance(customer_note, str):
            raise ValueError("Customer note must be a string.")

    if payment_data is not None and not isinstance(payment_data, list):
        raise ValueError("Payment data must be a list.")

    if expected_total is not None:
        expected_total = str(expected_total)

    data = {
        "billing_address": billing_address,
        "shipping_address": shipping_address,
        "payment_method": payment_method.strip(),
        "payment_data": payment_data or [],
    }

    if customer_note is not None:
        data["customer_note"] = customer_note

    if expected_total is not None:
        data["expected_total"] = expected_total

    response = client.request(
        "POST",
        "checkout",
        data=data,
    )

    if not isinstance(response, dict):
        raise StoreAPIError("Invalid order submission response.")

    if not response.get("order_id"):
        raise StoreAPIError(
            "Checkout response did not contain an order ID."
        )

    return response


def display_checkout(checkout: dict) -> None:
    """Display checkout information."""

    billing = checkout.get("billing_address") or {}
    shipping = checkout.get("shipping_address") or {}

    print("\n" + "=" * 65)
    print("                 NOREVIA CHECKOUT")
    print("=" * 65)

    print("\nBILLING INFORMATION")
    print("-" * 65)

    print(
        "Customer Name : "
        f"{billing.get('first_name', '')} "
        f"{billing.get('last_name', '')}"
    )
    print(f"Email         : {billing.get('email', 'N/A')}")
    print(f"Phone         : {billing.get('phone', 'N/A')}")
    print(f"Address       : {billing.get('address_1', 'N/A')}")
    print(f"City          : {billing.get('city', 'N/A')}")
    print(f"Country       : {billing.get('country', 'N/A')}")

    print("\nSHIPPING INFORMATION")
    print("-" * 65)

    print(
        "Recipient     : "
        f"{shipping.get('first_name', '')} "
        f"{shipping.get('last_name', '')}"
    )
    print(f"Address       : {shipping.get('address_1', 'N/A')}")
    print(f"City          : {shipping.get('city', 'N/A')}")
    print(f"Country       : {shipping.get('country', 'N/A')}")

    print("\nPAYMENT INFORMATION")
    print("-" * 65)

    print(
        "Payment Method: "
        f"{checkout.get('payment_method') or 'Not selected'}"
    )

    print("=" * 65)


def display_order_confirmation(order: dict) -> None:
    """Display the result of a completed checkout."""

    print("\n" + "=" * 65)
    print("              ORDER CONFIRMATION")
    print("=" * 65)

    print(f"Order ID     : {order.get('order_id', 'N/A')}")
    print(f"Order Number : {order.get('order_number', 'N/A')}")
    print(f"Order Status : {order.get('status', 'N/A')}")

    payment_result = order.get("payment_result") or {}

    print(
        "Payment      : "
        f"{payment_result.get('payment_status', 'Not confirmed')}"
    )

    print("=" * 65)
