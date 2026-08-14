from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import get_categories
from app.schemas import CategoryReadSchema


async def get_categories_service(db: AsyncSession) -> list[CategoryReadSchema]:
    """Return list of all product categories in the shop."""
    categories = await get_categories(db)
    return [CategoryReadSchema.model_validate(c) for c in categories]
