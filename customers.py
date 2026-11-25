from api_client import WooCommerceClient, WooCommerceAPIError


def get_customers(client: WooCommerceClient, per_page: int = 10):
    """Retrieve customers from WooCommerce."""

    if not isinstance(per_page, int) or not 1 <= per_page <= 100:
        raise ValueError("per_page must be between 1 and 100.")

    return client.request(
        "GET",
        "customers",
        params={"per_page": per_page},
    )


def get_customer_by_id(client: WooCommerceClient, customer_id: int):
    """Retrieve a customer using their ID."""

    if not isinstance(customer_id, int) or customer_id <= 0:
        raise ValueError("Customer ID must be a positive integer.")

    customer = client.request(
        "GET",
        f"customers/{customer_id}",
    )

    if not isinstance(customer, dict):
        raise WooCommerceAPIError("Invalid customer response.")

    return customer


def search_customers_by_email(
    client: WooCommerceClient,
    email: str,
):
    """Search WooCommerce customers by email address."""

    if not isinstance(email, str) or not email.strip():
        raise ValueError("Email address cannot be empty.")

    return client.request(
        "GET",
        "customers",
        params={"email": email.strip()},
    )


def create_customer(
    client: WooCommerceClient,
    email: str,
    first_name: str,
    last_name: str,
    username: str = "",
):
    """Create a new WooCommerce customer."""

    if not isinstance(email, str) or not email.strip():
        raise ValueError("Email address is required.")

    if not isinstance(first_name, str) or not first_name.strip():
        raise ValueError("First name is required.")

    if not isinstance(last_name, str) or not last_name.strip():
        raise ValueError("Last name is required.")

    customer_data = {
        "email": email.strip(),
        "first_name": first_name.strip(),
        "last_name": last_name.strip(),
    }

    if username.strip():
        customer_data["username"] = username.strip()

    return client.request(
        "POST",
        "customers",
        data=customer_data,
    )



def update_customer(
    client: WooCommerceClient,
    customer_id: int,
    customer_data: dict,
):
    """Update an existing WooCommerce customer."""

    if not isinstance(customer_id, int) or customer_id <= 0:
        raise ValueError("Customer ID must be a positive integer.")

    if not isinstance(customer_data, dict) or not customer_data:
        raise ValueError("Customer data must be a non-empty dictionary.")

    return client.request(
        "PUT",
        f"customers/{customer_id}",
        data=customer_data,
    )

def delete_customer(
    client: WooCommerceClient,
    customer_id: int,
    force: bool = False,
):
    """Delete a WooCommerce customer permanently."""

    if not isinstance(customer_id, int) or customer_id <= 0:
        raise ValueError("Customer ID must be a positive integer.")

    if force is not True:
        raise ValueError(
            "Permanent deletion requires force=True."
        )

    return client.request(
        "DELETE",
        f"customers/{customer_id}",
        params={"force": True},
    )


def display_customers(customers: list):
    """Display a list of WooCommerce customers."""

    if not customers:
        print("\nNo customers found.")
        return

    print("\n" + "=" * 75)
    print("                  NOREVIA CUSTOMER MANAGEMENT")
    print("=" * 75)

    for customer in customers:
        print(f"\nCustomer ID : {customer.get('id')}")
        print(
            "Name        : "
            f"{customer.get('first_name', '')} "
            f"{customer.get('last_name', '')}"
        )
        print(f"Email       : {customer.get('email', '')}")
        print(f"Username    : {customer.get('username', '')}")
        print("-" * 75)


def display_customer_details(customer: dict):
    """Display detailed customer information."""

    print("\n" + "=" * 60)
    print("                  CUSTOMER DETAILS")
    print("=" * 60)

    print(f"Customer ID : {customer.get('id')}")
    print(f"First Name  : {customer.get('first_name', '')}")
    print(f"Last Name   : {customer.get('last_name', '')}")
    print(f"Email       : {customer.get('email', '')}")
    print(f"Username    : {customer.get('username', '')}")

    billing = customer.get("billing", {})

    print("\nBILLING INFORMATION")
    print("-" * 60)
    print(f"Phone       : {billing.get('phone', '')}")
    print(f"City        : {billing.get('city', '')}")
    print(f"Country     : {billing.get('country', '')}")
