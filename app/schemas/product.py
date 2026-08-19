from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from .category import CategoryReadSchema


class ProductBase(BaseModel):
    """Base pydantic schema for product."""

    id: int
    name: str
    description: str | None = None
    price: Decimal
    categories: list[CategoryReadSchema]


class ProductReadSchema(ProductBase):
    """Pydantic schema for read data from ORM model."""

    model_config = ConfigDict(from_attributes=True)
