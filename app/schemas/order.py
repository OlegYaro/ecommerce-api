from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict

PaymentMethod = Literal["card", "cash"]
DeliveryMethod = Literal["courier", "inpost"]
OrderStatus = Literal["pending", "approved", "rejected"]


class OrderItemCreateSchema(BaseModel):
    """One line of the basket: what and how many."""

    product_id: int
    quantity: int


class OrderCreateSchema(BaseModel):
    """A new order as the customer sends it to the API."""

    items: list[OrderItemCreateSchema]
    payment_method: PaymentMethod
    delivery_method: DeliveryMethod
    billing_information: str


class OrderItemReadSchema(BaseModel):
    """One line of a stored order in order item."""

    product_id: int
    quantity: int
    price_at_purchase: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderReadSchema(BaseModel):
    """A stored order as the customer sees it no user_id, they know."""

    id: int
    status: OrderStatus
    payment_method: PaymentMethod
    delivery_method: DeliveryMethod
    billing_information: str
    total_amount: Decimal
    items: list[OrderItemReadSchema]

    model_config = ConfigDict(from_attributes=True)
