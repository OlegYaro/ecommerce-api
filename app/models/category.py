from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .product import Product


class Category(Base):
    """Orm class for table categories with definded id (as PK) and name (unique)."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    products: Mapped[list["Product"]] = relationship(
        secondary="product_categories",
        back_populates="categories",
        lazy="raise",
    )
