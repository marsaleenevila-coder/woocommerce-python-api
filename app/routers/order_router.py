
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Query,
)

from api_client import WooCommerceClient, WooCommerceAPIError

from app.core.dependencies import get_woocommerce_client

from app.schemas.order_schema import OrderResponseSchema

from app.services.order_service import (
    retrieve_orders,
    retrieve_order_by_id,
    find_orders_by_status,
)


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"],
)


# --------------------------------------------------
# 1. RETRIEVE ALL ORDERS WITH PAGINATION
# --------------------------------------------------

@router.get("/")
def get_all_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    client: WooCommerceClient = Depends(get_woocommerce_client),
):
    return retrieve_orders(
        client=client,
        page=page,
        per_page=per_page,
    )


# --------------------------------------------------
# 2. SEARCH ORDERS BY STATUS WITH PAGINATION
# --------------------------------------------------

@router.get("/search/status")
def search_orders_by_status(
    status: str = Query(
        ...,
        pattern="^(processing|completed|pending|on-hold|refunded|cancelled|failed)$",
    ),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    client: WooCommerceClient = Depends(get_woocommerce_client),
):
    return find_orders_by_status(
        client=client,
        status=status,
        page=page,
        per_page=per_page,
    )


# --------------------------------------------------
# 3. RETRIEVE ORDER BY ID
# --------------------------------------------------

@router.get(
    "/{order_id}",
    response_model=OrderResponseSchema,
)
def get_order_details(
    order_id: int = Path(..., gt=0),
    client: WooCommerceClient = Depends(get_woocommerce_client),
):
    try:
        order = retrieve_order_by_id(
            client=client,
            order_id=order_id,
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail=f"Order {order_id} was not found.",
            )

        return order

    except WooCommerceAPIError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error
