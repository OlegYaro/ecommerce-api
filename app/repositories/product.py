from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Product
from app.models.product_category import ProductCategory


async def get_products(
    db: AsyncSession, category_id: int | None = None, q: str | None = None
) -> list[Product]:
    """Fetches products from the database, optionally filtered by category_id."""
    stmt = select(Product).options(selectinload(Product.categories))
    if category_id is not None:
        stmt = stmt.join(
            ProductCategory, Product.id == ProductCategory.product_id
        ).where(ProductCategory.category_id == category_id)
    if q is not None:
        stmt = stmt.where(
            or_(Product.name.ilike(f"%{q}%"), Product.description.ilike(f"%{q}%"))
        )
    stmt = stmt.order_by(Product.name, Product.id)
    result = await db.execute(stmt)

    return list(result.scalars().all())


async def get_product(db: AsyncSession, product_id: int):
    """Fetches a single product by its ID from the database."""
    stmt = (
        select(Product)
        .options(selectinload(Product.categories))
        .where(Product.id == product_id)
    )
    result = await db.scalar(stmt)

    return result
