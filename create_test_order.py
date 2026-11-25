from store_api_client import WooCommerceStoreClient
from cart import add_to_cart, get_cart, remove_from_cart
from checkout import (
    update_customer_addresses,
    set_payment_method,
    submit_checkout,
    display_order_confirmation,
)

CONFIRM_ORDER = False

billing = {
    "first_name": "Test",
    "last_name": "Customer",
    "address_1": "1 Test Street",
    "city": "Madurai",
    "state": "TN",
    "postcode": "625001",
    "country": "IN",
    "email": "test@example.com",
    "phone": "0000000000",
}

shipping = {
    "first_name": "Test",
    "last_name": "Customer",
    "address_1": "1 Test Street",
    "city": "Madurai",
    "state": "TN",
    "postcode": "625001",
    "country": "IN",
}

with WooCommerceStoreClient() as client:
    item_key = None
    submission_attempted = False

    try:
        print("Initializing cart...")
        client.request("GET", "cart")

        print("Adding product...")
        cart = add_to_cart(client, 387, 1)

        item = next(
            (i for i in cart.get("items", []) if i.get("id") == 387),
            None,
        )

        if not item:
            raise RuntimeError("Product was not added.")

        item_key = item["key"]

        update_customer_addresses(
            client,
            billing,
            shipping,
        )

        set_payment_method(client, "cod")

        cart = get_cart(client)
        expected_total = str(cart["totals"]["total_price"])

        if expected_total != "79900":
            raise RuntimeError("Unexpected cart total.")

        print("Product:", item["name"])
        print("Total: INR 799.00")
        print("Payment: Cash on Delivery")

        if not CONFIRM_ORDER:
            print("\nOrder submission is disabled.")
            print("Set CONFIRM_ORDER = True after reviewing.")
        else:
            submission_attempted = True

            order = submit_checkout(
                client,
                billing_address=billing,
                shipping_address=shipping,
                payment_method="cod",
                customer_note="Norevia API integration test",
                expected_total=expected_total,
            )

            display_order_confirmation(order)

    except Exception as error:
        print("\nError:", error)

        if submission_attempted:
            print(
                "Check WooCommerce Admin > Orders before retrying."
            )

    finally:
        if item_key and not submission_attempted:
            try:
                remove_from_cart(client, item_key)
                print("\nTemporary cart item removed.")
            except Exception as error:
                print("\nCleanup error:", error)