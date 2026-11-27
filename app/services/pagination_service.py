from fastapi import HTTPException

from api_client import WooCommerceClient, WooCommerceAPIError


def get_paginated_records(
    client: WooCommerceClient,
    endpoint: str,
    page: int = 1,
    per_page: int = 10,
    params: dict | None = None,
) -> dict:
    """Retrieve one page of WooCommerce records with pagination metadata."""

    # Validate pagination parameters
    if page < 1:
        raise HTTPException(
            status_code=422,
            detail="Page must be greater than or equal to 1.",
        )

    if per_page < 1 or per_page > 100:
        raise HTTPException(
            status_code=422,
            detail="per_page must be between 1 and 100.",
        )

    # Prepare WooCommerce request parameters
    request_params = (params or {}).copy()
    request_params.update({
        "page": page,
        "per_page": per_page,
    })

    try:
        result = client.request(
            method="GET",
            endpoint=endpoint,
            params=request_params,
            return_metadata=True,
        )

        records = result["data"]

        if not isinstance(records, list):
            raise WooCommerceAPIError(
                "Expected a list of records from WooCommerce."
            )

        return {
            "page": page,
            "per_page": per_page,
            "total": result["total"],
            "total_pages": result["total_pages"],
            "items": records,
        }

    except WooCommerceAPIError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc
