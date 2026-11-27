
from api_client import WooCommerceClient

from app.services.pagination_service import get_paginated_records


def retrieve_products(
    client: WooCommerceClient,
    page: int = 1,
    per_page: int = 10,
):
    """Retrieve paginated WooCommerce products."""

    return get_paginated_records(
        client=client,
        endpoint="products",
        page=page,
        per_page=per_page,
        params={
            "orderby": "id",
            "order": "asc",
        },
    )


def find_products_by_name(
    client: WooCommerceClient,
    name: str,
    page: int = 1,
    per_page: int = 10,
):
    """Search products by name with pagination."""

    return get_paginated_records(
        client=client,
        endpoint="products",
        page=page,
        per_page=per_page,
        params={"search": name},
    )


def find_products_by_sku(
    client: WooCommerceClient,
    sku: str,
    page: int = 1,
    per_page: int = 10,
):
    """Search products by SKU with pagination."""

    return get_paginated_records(
        client=client,
        endpoint="products",
        page=page,
        per_page=per_page,
        params={"sku": sku},
    )


def find_products_by_keyword(
    client: WooCommerceClient,
    keyword: str,
    page: int = 1,
    per_page: int = 10,
):
    """Search products by keyword with pagination."""

    return get_paginated_records(
        client=client,
        endpoint="products",
        page=page,
        per_page=per_page,
        params={"search": keyword},
    )
