from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .category import Category


class Product(Base):
    """A product available for purchase in the shop.

    Defines the ``products`` table with id, name, description and price.
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    categories: Mapped[list["Category"]] = relationship(
        secondary="product_categories",
        back_populates="products",
        lazy="raise",
    )
