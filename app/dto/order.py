from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models import OrderStatus


class OrderItemCreateDTO(BaseModel):
    """A new order item as the customer sends it to the API."""

    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class OrderCreateDTO(BaseModel):
    """A new order as the customer sends it to the API."""

    items: list[OrderItemCreateDTO]
    payment_method: str
    delivery_method: str
    billing_information: str

    model_config = ConfigDict(from_attributes=True)


class OrderItemDTO(BaseModel):
    """One line of a stored order in order item."""

    product_id: int
    quantity: int
    price_at_purchase: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderDTO(BaseModel):
    """A stored order as the customer sees it no user_id, they know."""

    id: int
    user_id: int
    status: OrderStatus
    payment_method: str
    delivery_method: str
    billing_information: str
    total_amount: Decimal
    items: list[OrderItemDTO]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
