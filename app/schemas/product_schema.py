from pydantic import BaseModel, ConfigDict
from typing import Any


class ProductResponse(BaseModel):

    model_config = ConfigDict(extra="allow")

    id: int
    name: str
    type: str | None = None
    sku: str | None = None

    regular_price: str | None = None
    sale_price: str | None = None
    price: str | None = None

    stock_status: str | None = None
    stock_quantity: int | None = None

    description: str | None = None
    short_description: str | None = None

    permalink: str | None = None


class ProductListResponse(BaseModel):

    total: int
    products: list[dict[str, Any]]
