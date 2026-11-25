
from api_client import WooCommerceClient, WooCommerceAPIError

from products import get_products, display_products

from orders import (
    get_orders,
    get_order_by_id,
    get_orders_by_status,
    display_orders,
    display_order_details,
)


def main():
    try:
        client = WooCommerceClient()

        print("\nConnecting to WooCommerce...")
        print("Connection initialized successfully!")

        while True:
            print("\n" + "=" * 50)
            print("       NOREVIA WOOCOMMERCE API")
            print("=" * 50)
            print("1. Retrieve Products")
            print("2. Retrieve All Orders")
            print("3. Retrieve Order by ID")
            print("4. Search Orders by Status")
            print("5. Exit")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                products = get_products(client)
                display_products(products)

            elif choice == "2":
                orders = get_orders(client)
                display_orders(orders)

            elif choice == "3":
                order_id = int(input("Enter Order ID: "))
                order = get_order_by_id(client, order_id)
                display_order_details(order)

            elif choice == "4":
                status = input(
                    "Enter order status (processing, completed, pending): "
                ).strip()

                orders = get_orders_by_status(client, status)
                display_orders(orders)

            elif choice == "5":
                print("\nThank you for using Norevia WooCommerce API!")
                break

            else:
                print("\nInvalid choice. Please try again.")

    except (WooCommerceAPIError, ValueError) as error:
        print(f"\nError: {error}")

    except KeyboardInterrupt:
        print("\n\nApplication stopped by user.")

    except Exception as error:
        print(f"\nUnexpected Error: {error}")


if __name__ == "__main__":
    main()
