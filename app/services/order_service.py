
from api_client import WooCommerceClient

from orders import get_order_by_id

from app.services.pagination_service import get_paginated_records


def retrieve_orders(
    client: WooCommerceClient,
    page: int = 1,
    per_page: int = 10,
):
    """Retrieve paginated WooCommerce orders."""

    return get_paginated_records(
        client=client,
        endpoint="orders",
        page=page,
        per_page=per_page,
        params={
            "orderby": "date",
            "order": "desc",
        },
    )


def retrieve_order_by_id(
    client: WooCommerceClient,
    order_id: int,
):
    """Retrieve a single WooCommerce order by ID."""

    return get_order_by_id(client, order_id)


def find_orders_by_status(
    client: WooCommerceClient,
    status: str,
    page: int = 1,
    per_page: int = 10,
):
    """Retrieve paginated orders filtered by status."""

    return get_paginated_records(
        client=client,
        endpoint="orders",
        page=page,
        per_page=per_page,
        params={
            "status": status,
            "orderby": "date",
            "order": "desc",
        },
    )
