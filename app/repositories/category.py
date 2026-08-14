from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category


async def get_categories(db: AsyncSession) -> list[Category]:
    """Fetches all categories from the database, ordered by name."""
    statment = select(Category).order_by(Category.name)
    result = await db.execute(statment)

    return list(result.scalars().all())
