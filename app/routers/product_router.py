
from fastapi import APIRouter, Depends, Query

from api_client import WooCommerceClient

from app.core.dependencies import get_woocommerce_client

from app.services.product_service import (
    retrieve_products,
    find_products_by_name,
    find_products_by_sku,
    find_products_by_keyword,
)


router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"],
)


# --------------------------------------------------
# 1. RETRIEVE ALL PRODUCTS WITH PAGINATION
# --------------------------------------------------

@router.get("/")
def get_all_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    client: WooCommerceClient = Depends(get_woocommerce_client),
):
    return retrieve_products(
        client=client,
        page=page,
        per_page=per_page,
    )


# --------------------------------------------------
# 2. SEARCH PRODUCTS BY NAME
# --------------------------------------------------

@router.get("/search/name")
def search_by_name(
    name: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    client: WooCommerceClient = Depends(get_woocommerce_client),
):
    return find_products_by_name(
        client=client,
        name=name.strip(),
        page=page,
        per_page=per_page,
    )


# --------------------------------------------------
# 3. SEARCH PRODUCTS BY SKU
# --------------------------------------------------

@router.get("/search/sku")
def search_by_sku(
    sku: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    client: WooCommerceClient = Depends(get_woocommerce_client),
):
    return find_products_by_sku(
        client=client,
        sku=sku.strip(),
        page=page,
        per_page=per_page,
    )


# --------------------------------------------------
# 4. SEARCH PRODUCTS BY KEYWORD
# --------------------------------------------------

@router.get("/search/keyword")
def search_by_keyword(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    client: WooCommerceClient = Depends(get_woocommerce_client),
):
    return find_products_by_keyword(
        client=client,
        keyword=keyword.strip(),
        page=page,
        per_page=per_page,
    )
