from api_client import WooCommerceClient, WooCommerceAPIError
from products import get_products, display_products


def main():
    try:
        client = WooCommerceClient()

        print("Connecting to WooCommerce...")

        products = get_products(client)

        display_products(products)

    except WooCommerceAPIError as error:
        print(f"\nWooCommerce API Error: {error}")

    except Exception as error:
        print(f"\nUnexpected Error: {error}")


if __name__ == "__main__":
    main()

