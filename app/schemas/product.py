from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    """Base pydantic schema for product."""

    id: int
    name: str
    description: str | None = None
    price: Decimal
    created_at: datetime
    updated_at: datetime


class ProductReadSchema(ProductBase):
    """Pydantic schema for read data from ORM model."""

    model_config = ConfigDict(from_attributes=True)
