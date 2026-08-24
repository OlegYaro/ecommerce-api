from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Order(Base):
    """An order submitted by a customer."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), index=True
    )
    status: Mapped[str] = mapped_column(String(16), default="pending")
    payment_method: Mapped[str] = mapped_column(String(16))
    delivery_method: Mapped[str] = mapped_column(String(16))
    billing_information: Mapped[str] = mapped_column(Text)

    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan", lazy="raise"
    )


class OrderItem(Base):
    """One product line of an order, with the price frozen at purchase."""

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), index=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT")
    )
    quantity: Mapped[int]
    price_at_purchase: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    order: Mapped["Order"] = relationship(back_populates="items", lazy="raise")
