from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Product
from app.models.product_category import ProductCategory


async def get_products(
    db: AsyncSession,
    category_id: int | None = None,
) -> list[Product]:
    """Fetches products from the database, optionally filtered by category_id."""
    stmt = select(Product).options(selectinload(Product.categories))
    if category_id is not None:
        stmt = stmt.join(
            ProductCategory, Product.id == ProductCategory.product_id
        ).where(ProductCategory.category_id == category_id)
    stmt = stmt.order_by(Product.name, Product.id)
    result = await db.execute(stmt)

    return list(result.scalars().all())
