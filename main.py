from api_client import WooCommerceClient, WooCommerceAPIError

from products import (
    get_products,
    display_products,
    search_products_by_name,
    search_products_by_sku,
    search_products_by_keyword,
)

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
            print("\n" + "=" * 60)
            print("              NOREVIA WOOCOMMERCE API")
            print("=" * 60)

            print("\nPRODUCT MANAGEMENT")
            print("1. Retrieve All Products")
            print("2. Search Products by Name")
            print("3. Search Products by SKU")
           
            print("\nORDER MANAGEMENT")
            print("4. Retrieve All Orders")
            print("5. Retrieve Order by ID")
            print("6. Search Orders by Status")

            # print("\nCUSTOMER MANAGEMENT")
            # print("7. Retrieve All Customers")
            # print("8. Retrieve Customer by ID")
            # print("9. Search Customers by Email")
            # print("10. Retrieve Store Configuration")

            print("\n7. Exit")

            choice = input("\nEnter your choice: ").strip()

            # ------------------------------------------
            # 1. RETRIEVE ALL PRODUCTS
            # ------------------------------------------

            if choice == "1":

                products = get_products(client)

                display_products(products)

            # ------------------------------------------
            # 2. SEARCH PRODUCTS BY NAME
            # ------------------------------------------

            elif choice == "2":

                name = input(
                    "\nEnter product name to search: "
                ).strip()

                products = search_products_by_name(
                    client,
                    name
                )

                print("\n" + "=" * 90)
                print("             NOREVIA - PRODUCT NAME SEARCH RESULTS")
                print("=" * 90)

                display_products(products)

            # ------------------------------------------
            # 3. SEARCH PRODUCTS BY SKU
            # ------------------------------------------

            elif choice == "3":

                sku = input(
                    "\nEnter product SKU to search: "
                ).strip()

                products = search_products_by_sku(
                    client,
                    sku
                )

                print("\n" + "=" * 90)
                print("                NOREVIA - SKU SEARCH RESULTS")
                print("=" * 90)

                display_products(products)

            # ------------------------------------------
            # 4. RETRIEVE ALL ORDERS
            # ------------------------------------------

            elif choice == "4":

                orders = get_orders(client)

                display_orders(client, orders)

            # ------------------------------------------
            #  5. RETRIEVE ORDER BY ID
            # ------------------------------------------

            elif choice == "5":

                order_id = int(
                    input("\nEnter Order ID: ")
                )

                order = get_order_by_id(
                    client,
                    order_id
                )

                display_order_details(client, order)

            # ------------------------------------------
            # 6. SEARCH ORDERS BY STATUS
            # ------------------------------------------

            elif choice == "6":

                status = input(
                    "\nEnter order status "
                    "(processing, completed, pending, on-hold, "
                    "refunded, cancelled, failed): "
                ).strip().lower()

                orders = get_orders_by_status(
                    client,
                    status
                )

                display_orders(client, orders)

            # ------------------------------------------
            # CUSTOMER MANAGEMENT
            # ------------------------------------------

            # elif choice == "7":
            #     customers = get_customers(client)
            #     print(f"\nTotal customers retrieved: {len(customers)}")
            #     display_customers(customers)

            # elif choice == "8":
            #     customer_id = int(input("Enter Customer ID: "))
            #     customer = get_customer_by_id(client, customer_id)
            #     display_customer_details(customer)

            # elif choice == "9":
            #     email = input("Enter customer email: ").strip()
            #     customers = search_customers_by_email(client, email)
            #     print(f"\nCustomers found: {len(customers)}")
            #     display_customers(customers)

            # elif choice == "10":
            #     configuration = get_store_configuration(client)
            #     display_store_configuration(configuration)

            # ------------------------------------------
            # 8. EXIT
            # ------------------------------------------

            elif choice == "7":

                print(
                    "\nThank you for using "
                    "Norevia WooCommerce API!"
                )

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
