from api_client import WooCommerceClient


def get_woocommerce_client() -> WooCommerceClient:
    """
    Create a WooCommerce API client.
    """

    return WooCommerceClient()
