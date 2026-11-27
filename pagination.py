from api_client import WooCommerceClient, WooCommerceAPIError


PER_PAGE = 10


def fetch_all_pages(
    client: WooCommerceClient,
    endpoint: str,
    params: dict | None = None,
    per_page: int = PER_PAGE,
) -> list:
    """Retrieve all API records in batches using pagination."""

    if per_page < 1 or per_page > 100:
        raise ValueError("per_page must be between 1 and 100.")

    all_records = []
    page = 1

    while True:
        request_params = (params or {}).copy()

        request_params.update({
            "per_page": per_page,
            "page": page,
        })

        print(f"Retrieving {endpoint}: Page {page}...")

        response = client.request(
            method="GET",
            endpoint=endpoint,
            params=request_params,
        )

        if not isinstance(response, list):
            raise WooCommerceAPIError(
                f"Invalid response while retrieving {endpoint}."
            )

        if not response:
            break

        all_records.extend(response)

        print(
            f"Retrieved {len(response)} records "
            f"(Total: {len(all_records)})"
        )

        if len(response) < per_page:
            break

        page += 1

    return all_records
