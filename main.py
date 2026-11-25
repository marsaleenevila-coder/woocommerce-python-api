from api_client import WooCommerceClient, WooCommerceAPIError

from products import get_products, display_products

from orders import (
    get_orders,
    get_order_by_id,
    get_orders_by_status,
    display_orders,
    display_order_details,
)

from customers import (
    get_customers,
    get_customer_by_id,
    search_customers_by_email,
    display_customers,
    display_customer_details,
)

from store_config import (
    get_store_configuration,
    display_store_configuration,
)

def main():
    try:
        client = WooCommerceClient()

        print("\nConnecting to WooCommerce...")
        print("Connection initialized successfully!")

        while True:
            print("\n" + "=" * 55)
            print("          NOREVIA WOOCOMMERCE API")
            print("=" * 55)

            print("\nPRODUCT MANAGEMENT")
            print("1. Retrieve Products")

            print("\nORDER MANAGEMENT")
            print("2. Retrieve All Orders")
            print("3. Retrieve Order by ID")
            print("4. Search Orders by Status")

            print("\nCUSTOMER MANAGEMENT")
            print("5. Retrieve All Customers")
            print("6. Retrieve Customer by ID")
            print("7. Search Customers by Email")
            print("8. Retrieve Store Configuration")
            print("\n9. Exit")

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
                customers = get_customers(client)
                print(f"\nTotal customers retrieved: {len(customers)}")
                display_customers(customers)

            elif choice == "6":
                customer_id = int(input("Enter Customer ID: "))
                customer = get_customer_by_id(client, customer_id)
                display_customer_details(customer)

            elif choice == "7":
                email = input("Enter customer email: ").strip()
                customers = search_customers_by_email(client, email)

                print(f"\nCustomers found: {len(customers)}")
                display_customers(customers)

            elif choice == "8":
                configuration = get_store_configuration(client)
                display_store_configuration(configuration)

            elif choice == "9":
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