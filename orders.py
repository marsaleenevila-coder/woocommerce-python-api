from api_client import WooCommerceClient, WooCommerceAPIError
from pagination import fetch_all_pages

def create_order(
    client: WooCommerceClient,
    product_id: int,
    quantity: int,
    status: str,
    customer_name: str = "Test Customer",
    customer_email: str = "test@example.com",
) -> dict:
    """Create a WooCommerce order."""

    allowed_statuses = {
        "processing",
        "completed",
        "pending",
        "on-hold",
        "refunded",
        "cancelled",
        "failed",
    }

    if status not in allowed_statuses:
        raise ValueError(f"Unsupported order status: {status}")

    if product_id <= 0 or quantity <= 0:
        raise ValueError("Product ID and quantity must be positive.")

    first_name, _, last_name = customer_name.partition(" ")

    order_data = {
        "status": status,
        "currency": "INR",
        "payment_method": "cod",
        "payment_method_title": "Cash on delivery",
        "set_paid": False,
        "billing": {
            "first_name": first_name,
            "last_name": last_name,
            "email": customer_email,
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
            "Invalid API response while creating order."
        )

    return response


def create_test_orders(client: WooCommerceClient) -> list:
    """Create ten test orders with different statuses."""

    order_statuses = [
        "processing",
        "completed",
        "pending",
        "on-hold",
        "processing",
        "refunded",
        "cancelled",
        "failed",
        "completed",
        "pending",
    ]

    created_orders = []

    for status in order_statuses:
        order = create_order(
            client=client,
            product_id=387,
            quantity=1,
            status=status,
        )

        created_orders.append(order)

        print(
            f"Created Order ID: {order['id']} "
            f"| Status: {order['status']} "
            f"| Total: {order.get('total', 'N/A')}"
        )

    return created_orders


def get_orders(client: WooCommerceClient) -> list:
    """Retrieve all WooCommerce orders using pagination."""

    orders = fetch_all_pages(
        client=client,
        endpoint="orders",
        params={
            "orderby": "date",
            "order": "desc",
        },
        per_page=10,
    )

    print(f"\nTotal orders retrieved: {len(orders)}")

    return orders


def get_order_by_id(
    client: WooCommerceClient,
    order_id: int,
) -> dict:
    """Retrieve a WooCommerce order by ID."""

    if order_id <= 0:
        raise ValueError("Order ID must be positive.")

    response = client.request(
        method="GET",
        endpoint=f"orders/{order_id}",
    )

    if not isinstance(response, dict) or "id" not in response:
        raise WooCommerceAPIError(
            f"Invalid API response while retrieving order {order_id}."
        )

    return response


def get_orders_by_status(
    client: WooCommerceClient,
    status: str,
) -> list:
    """Retrieve orders filtered by status using pagination."""

    allowed_statuses = {
        "processing",
        "completed",
        "pending",
        "on-hold",
        "refunded",
        "cancelled",
        "failed",
    }

    if status not in allowed_statuses:
        raise ValueError("Invalid order status.")

    orders = fetch_all_pages(
        client=client,
        endpoint="orders",
        params={
            "status": status,
            "orderby": "date",
            "order": "desc",
        },
        per_page=10,
    )

    print(
        f"\nTotal orders with status '{status}': "
        f"{len(orders)}"
    )

    return orders

def display_orders(client: WooCommerceClient, orders: list) -> None:
    """Display WooCommerce orders with product stock status."""

    print("\n" + "=" * 100)
    print("                         NOREVIA - ORDER LIST")
    print("=" * 100)

    for order in orders:
        print(f"\nOrder ID       : {order.get('id')}")
        #print(f"Order Number   : {order.get('number')}")

        billing = order.get("billing", {})
        customer_name = (
            f"{billing.get('first_name', '')} "
            f"{billing.get('last_name', '')}"
        ).strip()

        print(f"Customer       : {customer_name or 'Guest'}")
        print(f"Email          : {billing.get('email', 'N/A')}")
        print(f"Total          : ₹{order.get('total', '0')}")

        print("\nPRODUCT DETAILS")
        print("-" * 100)

        for item in order.get("line_items", []):
            product_id = item.get("product_id")
            product = client.request(
                method="GET",
                endpoint=f"products/{product_id}",
            )

            stock_status = product.get("stock_status", "N/A")

            if stock_status == "instock":
                stock_status = "In Stock"
            elif stock_status == "outofstock":
                stock_status = "Out of Stock"
            else:
                stock_status = "N/A"

            print(f"Product        : {item.get('name')}")
            print(f"Quantity       : {item.get('quantity')}")
            print(f"Stock Status   : {stock_status}")
            print("-" * 100)

def get_product_stock_status(product_id: int) -> dict:
    """Retrieve product stock status from WooCommerce."""

    client = WooCommerceClient()

    response = client.request(
        method="GET",
        endpoint=f"products/{product_id}",
    )

    if not isinstance(response, dict):
        raise WooCommerceAPIError(
            f"Unable to retrieve product ID {product_id}."
        )

    return response
def display_order_details(client: WooCommerceClient, order: dict) -> None:
    """Display detailed order information with product stock status."""

    billing = order.get("billing", {})

    print("\n" + "=" * 70)
    print("               NOREVIA - ORDER DETAILS")
    print("=" * 70)

    print(f"\nOrder ID       : {order.get('id')}")
    # print(f"Order Number   : {order.get('number')}")
    print(f"Currency       : {order.get('currency')}")
    print(f"Total          : ₹{order.get('total')}")
    print(f"Payment Method : {order.get('payment_method_title')}")
    print(f"Date Created   : {order.get('date_created')}")

    print("\nCUSTOMER DETAILS")
    print("-" * 70)
    print(
        f"Name           : "
        f"{billing.get('first_name', '')} "
        f"{billing.get('last_name', '')}"
    )
    print(f"Email          : {billing.get('email', 'N/A')}")
    print(f"Phone          : {billing.get('phone', 'N/A')}")

    print("\nPRODUCT DETAILS")
    print("-" * 70)

    for item in order.get("line_items", []):
        product_id = item.get("product_id")

        product = client.request(
            method="GET",
            endpoint=f"products/{product_id}",
        )

        stock_status = product.get("stock_status", "N/A")

        if stock_status == "instock":
            stock_status = "In Stock"
        elif stock_status == "outofstock":
            stock_status = "Out of Stock"
        else:
            stock_status = "N/A"

        print(f"Product Name   : {item.get('name')}")
        print(f"Product ID     : {product_id}")
        print(f"Quantity       : {item.get('quantity')}")
        print(f"Stock Status   : {stock_status}")
        print(f"Item Total     : ₹{item.get('total')}")
        print("-" * 70)

    print("=" * 70)