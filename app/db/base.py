"""import all the models for alembic to detect them."""

from app.db.base_class import Base  # noqa: F401
from app.models import (
    Category,  # noqa: F401
    Order,  # noqa: F401
    OrderItem,  # noqa: F401
    Product,  # noqa: F401
    ProductCategory,  # noqa: F401
    User,  # noqa: F401
)
