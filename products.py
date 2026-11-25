from api_client import WooCommerceClient, WooCommerceAPIError


def get_products(client: WooCommerceClient, per_page: int = 10) -> list:
    """
    Retrieve all published products from WooCommerce.

    Args:
        client: Authenticated WooCommerce API client.
        per_page: Number of products requested per page.

    Returns:
        List of published products.
    """
    products = []
    page = 1

    while True:
        response = client.request(
            method="GET",
            endpoint="products",
            params={
                "status": "publish",
                "per_page": per_page,
                "page": page,
            },
        )

        if not isinstance(response, list):
            raise WooCommerceAPIError(
                "Invalid API response: expected a list of products."
            )

        if not response:
            break

        products.extend(response)

        if len(response) < per_page:
            break

        page += 1

    return products


def display_products(products: list) -> None:
    """Display WooCommerce product details in a readable format."""

    if not products:
        print("\nNo published products found.")
        return

    print("\n" + "=" * 70)
    print("                 WOOCOMMERCE PUBLISHED PRODUCTS")
    print("=" * 70)

    for product in products:
        print(f"\nProduct ID      : {product.get('id', 'N/A')}")
        print(f"Name            : {product.get('name') or 'N/A'}")
        print(f"SKU             : {product.get('sku') or 'Not assigned'}")
        print(f"Regular Price   : {product.get('regular_price') or 'N/A'}")
        print(f"Sale Price      : {product.get('sale_price') or 'N/A'}")
        print(f"Stock Quantity  : {product.get('stock_quantity') if product.get('stock_quantity') is not None else 'Not managed'}")
        print(f"Status          : {product.get('status') or 'N/A'}")
        print("-" * 70)

    print(f"\nTotal products: {len(products)}")


def search_products_by_name(
    client: WooCommerceClient,
    name: str
) -> list:
    """Search published products by product name."""

    if not name.strip():
        raise ValueError("Product name cannot be empty.")

    response = client.request(
        method="GET",
        endpoint="products",
        params={
            "status": "publish",
            "search": name.strip(),
            "per_page": 100,
        },
    )

    if not isinstance(response, list):
        raise WooCommerceAPIError(
            "Invalid API response: expected a list of products."
        )

    return response


def search_products_by_sku(
    client: WooCommerceClient,
    sku: str
) -> list:
    """Search published products by SKU."""

    if not sku.strip():
        raise ValueError("Product SKU cannot be empty.")

    response = client.request(
        method="GET",
        endpoint="products",
        params={
            "status": "publish",
            "sku": sku.strip(),
            "per_page": 100,
        },
    )

    if not isinstance(response, list):
        raise WooCommerceAPIError(
            "Invalid API response: expected a list of products."
        )

    return response
