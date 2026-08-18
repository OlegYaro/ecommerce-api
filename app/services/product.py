from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import get_product, get_products
from app.schemas import ProductReadSchema


async def get_products_service(
    db: AsyncSession, category_id: int | None = None, q: str | None = None
) -> list[ProductReadSchema]:
    """Return list of all products by categoryin the shop."""
    products = await get_products(db, category_id, q)
    return [ProductReadSchema.model_validate(p) for p in products]


async def get_product_service(db: AsyncSession, product_id: int):
    """Return product by id."""
    product = await get_product(db, product_id)
    return ProductReadSchema.model_validate(product) if product else None
