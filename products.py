from api_client import WooCommerceClient, WooCommerceAPIError
from pagination import fetch_all_pages


def get_products(client: WooCommerceClient) -> list:
    """Retrieve all WooCommerce products using pagination."""

    products = fetch_all_pages(
        client=client,
        endpoint="products",
        params={
            "orderby": "id",
            "order": "asc",
        },
        per_page=10,
    )

    print(f"\nTotal products retrieved: {len(products)}")

    return products

def display_products(products: list) -> None:
    """Display WooCommerce products."""

    if not products:
        print("\nNo products found.")
        return

    print("\n" + "=" * 100)
    print("                    NOREVIA - PRODUCT CATALOGUE")
    print("=" * 100)

    for product in products:
        stock_status = product.get("stock_status", "N/A")

        if stock_status == "instock":
            stock_status = "In Stock"
        elif stock_status == "outofstock":
            stock_status = "Out of Stock"
        else:
            stock_status = "N/A"

        print(f"\nProduct ID      : {product.get('id')}")
        print(f"Product Name    : {product.get('name')}")
        print(f"SKU             : {product.get('sku') or 'N/A'}")
        print(f"Regular Price   : ₹{product.get('regular_price') or 'N/A'}")
        print(f"Sale Price      : ₹{product.get('sale_price') or 'N/A'}")
        print(f"Current Price   : ₹{product.get('price') or 'N/A'}")
        print(f"Stock Status    : {stock_status}")
        print("-" * 100)

    print(f"\nTotal products displayed: {len(products)}")

def display_product_details(product: dict) -> None:
    """Display complete details of one WooCommerce product."""

    tags = product.get("tags", [])
    categories = product.get("categories", [])

    tag_names = ", ".join(
        tag.get("name", "") for tag in tags
    ) or "No tags assigned"

    category_names = ", ".join(
        category.get("name", "") for category in categories
    ) or "Uncategorized"

    if not isinstance(product, dict):
        return

    stock_status = product.get("stock_status", "N/A")

    stock_labels = {
        "instock": "In Stock",
        "outofstock": "Out of Stock",
        "onbackorder": "On Backorder",
    }

    stock_status = stock_labels.get(stock_status, stock_status)

    stock_quantity = product.get("stock_quantity")

    print(f"\nProduct ID      : {product.get('id', 'N/A')}")
    print(f"Product Name    : {product.get('name') or 'N/A'}")
    print(f"SKU             : {product.get('sku') or 'Not assigned'}")
    print(f"Regular Price   : {product.get('regular_price') or 'N/A'}")
    print(f"Sale Price      : {product.get('sale_price') or 'N/A'}")
    print(f"Current Price   : {product.get('price') or 'N/A'}")

    print(
        f"Stock Quantity  : "
        f"{stock_quantity if stock_quantity is not None else 'Not managed'}"
    )

    print(f"Stock Status    : {stock_status}")
    print(f"Product Status  : {product.get('status', 'N/A')}")
    print(f"Product Type    : {product.get('type', 'N/A')}")

    print("-" * 90)



def search_products_by_name(
    client: WooCommerceClient,
    name: str
) -> list:
    """
    Search published products using product name only.
    Tags, categories and descriptions are ignored.
    """

    if not name or not name.strip():
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

    search_term = name.strip().casefold()

    # Verify that the keyword exists in the product name only.
    matching_products = [
        product for product in response
        if search_term in (product.get("name") or "").casefold()
    ]

    return matching_products


def search_products_by_sku(
    client: WooCommerceClient,
    sku: str
) -> list:
    """Search published products using their exact SKU."""

    if not sku or not sku.strip():
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

    # Verify exact SKU matches.
    exact_matches = [
        product for product in response
        if (product.get("sku") or "").strip().casefold()
        == sku.strip().casefold()
    ]

    return exact_matches



def search_products_by_keyword(
    client: WooCommerceClient,
    keyword: str
) -> list:
    """
    Search published products by keyword across:
    - Product name
    - Product tags
    - Product categories
    - Product description
    - Short description
    """

    if not keyword or not keyword.strip():
        raise ValueError("Search keyword cannot be empty.")

    keyword = keyword.strip().casefold()

    # Retrieve all published products
    products = get_products(client, per_page=100)

    matching_products = []

    for product in products:

        product_name = product.get("name", "")
        description = product.get("description", "")
        short_description = product.get("short_description", "")

        tags = [
            tag.get("name", "")
            for tag in product.get("tags", [])
        ]

        categories = [
            category.get("name", "")
            for category in product.get("categories", [])
        ]

        searchable_content = [
            product_name,
            description,
            short_description,
            *tags,
            *categories,
        ]

        # Match keyword in any product field
        if any(
            keyword in str(value).casefold()
            for value in searchable_content
        ):
            matching_products.append(product)

    return matching_products


def update_product_stock_status(
    client: WooCommerceClient,
    product_id: int,
    stock_status: str,
) -> dict:
    """Update a product's stock status."""

    allowed_statuses = {"instock", "outofstock"}

    if stock_status not in allowed_statuses:
        raise ValueError(
            "Stock status must be instock or outofstock."
        )

    response = client.request(
        method="PUT",
        endpoint=f"products/{product_id}",
        data={"stock_status": stock_status},
    )

    if not isinstance(response, dict) or "id" not in response:
        raise WooCommerceAPIError(
            "Failed to update product stock status."
        )

    return response
