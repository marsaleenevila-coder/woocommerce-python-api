from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class OrderLineItemSchema(BaseModel):

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    product_id: int | None = None
    name: str | None = None
    sku: str | None = None
    quantity: int | None = None
    price: Any = None
    subtotal: str | None = None
    total: str | None = None


class OrderResponseSchema(BaseModel):

    model_config = ConfigDict(extra="allow")

    id: int
    status: str

    currency: str | None = None
    total: str | None = None

    customer_id: int | None = None
    date_created: str | None = None

    payment_method: str | None = None
    payment_method_title: str | None = None

    billing: dict[str, Any] | None = None
    shipping: dict[str, Any] | None = None

    line_items: list[OrderLineItemSchema] = Field(
        default_factory=list
    )


class OrderListResponseSchema(BaseModel):

    total: int
    orders: list[OrderResponseSchema]
