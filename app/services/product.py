from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import get_products
from app.schemas import ProductReadSchema


async def get_products_service(
    db: AsyncSession, category_id: int | None = None, q: str | None = None
) -> list[ProductReadSchema]:
    """Return list of all products by categoryin the shop."""
    products = await get_products(db, category_id, q)
    return [ProductReadSchema.model_validate(p) for p in products]
