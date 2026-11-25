
import httpx

from config import WC_STORE_URL, WC_TIMEOUT


def get_store_configuration(client):
    """Retrieve store information and enabled payment gateways."""

    # Retrieve WordPress site information.
    try:
        response = httpx.get(
            f"{WC_STORE_URL}/wp-json/",
            timeout=WC_TIMEOUT,
        )
        response.raise_for_status()
        store_info = response.json()

    except httpx.HTTPError as exc:
        raise ValueError(
            f"Could not retrieve WordPress site information: {exc}"
        ) from exc

    if not isinstance(store_info, dict):
        raise ValueError("Invalid WordPress site information received.")

    # Retrieve WooCommerce general settings.
    general_settings = client.request("GET", "settings/general")

    # Retrieve available payment gateways.
    payment_gateways = client.request("GET", "payment_gateways")

    if not isinstance(general_settings, list):
        raise ValueError("Invalid general settings received.")

    if not isinstance(payment_gateways, list):
        raise ValueError("Invalid payment gateway information received.")

    # Convert settings into an ID/value dictionary.
    settings = {
        setting.get("id"): setting.get("value")
        for setting in general_settings
        if isinstance(setting, dict) and setting.get("id")
    }

    # Extract country code.
    base_country = settings.get("woocommerce_default_country", "")
    country_code = (
        base_country.split(":")[0]
        if base_country
        else "Not configured"
    )

    # Filter enabled payment gateways.
    enabled_gateways = [
        gateway
        for gateway in payment_gateways
        if isinstance(gateway, dict)
        and gateway.get("enabled") is True
    ]

    return {
        "store_name": store_info.get("name", "Not available"),
        "store_url": store_info.get("url", "Not available"),
        "currency": settings.get(
            "woocommerce_currency", "Not configured"
        ),
        "country": country_code,
        "payment_gateways": enabled_gateways,
    }


def display_store_configuration(configuration):
    """Display store configuration in the terminal."""

    print("\n" + "=" * 55)
    print("             NOREVIA STORE CONFIGURATION")
    print("=" * 55)

    print(f"Store Name : {configuration['store_name']}")
    print(f"Store URL  : {configuration['store_url']}")
    print(f"Currency   : {configuration['currency']}")
    print(f"Country    : {configuration['country']}")

    print("\nENABLED PAYMENT GATEWAYS")
    print("-" * 55)

    gateways = configuration["payment_gateways"]

    if not gateways:
        print("No enabled payment gateways found.")
    else:
        for number, gateway in enumerate(gateways, start=1):
            title = (
                gateway.get("title")
                or gateway.get("method_title")
                or "Unknown"
            )
            gateway_id = gateway.get("id", "Unknown")

            print(f"{number}. {title} ({gateway_id})")

    print("=" * 55)
