from api_client import WooCommerceClient, WooCommerceAPIError


def get_orders(
    client: WooCommerceClient,
    per_page: int = 10,
    status: str | None = None
) -> list:
    """
    Retrieve WooCommerce orders.

    Args:
        client: Authenticated WooCommerce API client.
        per_page: Number of orders per API page.
        status: Optional order status filter.

    Returns:
        List of WooCommerce orders.
    """

    if not 1 <= per_page <= 100:
        raise ValueError("per_page must be between 1 and 100.")

    orders = []
    page = 1

    while True:
        params = {
            "per_page": per_page,
            "page": page,
        }

        if status:
            params["status"] = status

        response = client.request(
            method="GET",
            endpoint="orders",
            params=params
        )

        if not isinstance(response, list):
            raise WooCommerceAPIError(
                "Invalid API response: expected a list of orders."
            )

        if not response:
            break

        orders.extend(response)

        if len(response) < per_page:
            break

        page += 1

    return orders


def get_order_by_id(
    client: WooCommerceClient,
    order_id: int
) -> dict:
    """Retrieve a specific WooCommerce order by ID."""

    if order_id <= 0:
        raise ValueError("Order ID must be a positive integer.")

    response = client.request(
        method="GET",
        endpoint=f"orders/{order_id}"
    )

    if not isinstance(response, dict):
        raise WooCommerceAPIError(
            "Invalid API response: expected an order object."
        )

    return response


def get_orders_by_status(
    client: WooCommerceClient,
    status: str
) -> list:
    """Retrieve orders filtered by their status."""

    if not status.strip():
        raise ValueError("Order status cannot be empty.")

    return get_orders(
        client=client,
        status=status.strip()
    )


def display_orders(orders: list) -> None:
    """Display WooCommerce order information."""

    if not orders:
        print("\nNo orders found.")
        return

    print("\n" + "=" * 75)
    print("                    WOOCOMMERCE ORDERS")
    print("=" * 75)

    for order in orders:
        billing = order.get("billing") or {}

        customer_name = (
            f"{billing.get('first_name', '')} "
            f"{billing.get('last_name', '')}"
        ).strip()

        print(f"\nOrder ID       : {order.get('id', 'N/A')}")
        print(f"Order Number   : {order.get('number', 'N/A')}")
        print(f"Customer       : {customer_name or 'Guest'}")
        print(f"Email          : {billing.get('email', 'N/A')}")
        print(f"Status         : {order.get('status', 'N/A')}")
        print(f"Currency       : {order.get('currency', 'N/A')}")
        print(f"Total          : {order.get('total', 'N/A')}")
        print(f"Payment Method : {order.get('payment_method_title', 'N/A')}")
        print(f"Date Created   : {order.get('date_created', 'N/A')}")
        print("-" * 75)

    print(f"\nTotal orders: {len(orders)}")


def display_order_details(order: dict) -> None:
    """Display detailed information about one order."""

    print("\n" + "=" * 75)
    print("                   WOOCOMMERCE ORDER DETAILS")
    print("=" * 75)

    print(f"Order ID       : {order.get('id', 'N/A')}")
    print(f"Order Number   : {order.get('number', 'N/A')}")
    print(f"Status         : {order.get('status', 'N/A')}")
    print(f"Currency       : {order.get('currency', 'N/A')}")
    print(f"Total          : {order.get('total', 'N/A')}")
    print(f"Payment Method : {order.get('payment_method_title', 'N/A')}")

    billing = order.get("billing") or {}

    print("\nCUSTOMER INFORMATION")
    print("-" * 75)
    print(
        "Name           : "
        f"{billing.get('first_name', '')} "
        f"{billing.get('last_name', '')}"
    )
    print(f"Email          : {billing.get('email', 'N/A')}")
    print(f"Phone          : {billing.get('phone', 'N/A')}")

    print("\nORDER ITEMS")
    print("-" * 75)

    for item in order.get("line_items", []):
        print(f"Product        : {item.get('name', 'N/A')}")
        print(f"Quantity       : {item.get('quantity', 0)}")
        print(f"Total          : {item.get('total', 'N/A')}")
        print("-" * 75)
