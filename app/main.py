
from fastapi import FastAPI

from app.routers import (
    product_router,
    order_router,
)


app = FastAPI(
    title="Norevia WooCommerce API",
    description=(
        "REST API for Norevia Technologies "
        "WooCommerce store management."
    ),
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "Welcome to Norevia WooCommerce API",
        "status": "running",
        "documentation": "/docs"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# PRODUCT ROUTER

app.include_router(
    product_router.router
)


# ORDER ROUTER

app.include_router(
    order_router.router
)
