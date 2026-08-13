from fastapi import APIRouter

from app.api.deps import DbSession
from app.repositories import get_categories
from app.schemas import CategoryReadSchema

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
async def list_categories(db: DbSession) -> list[CategoryReadSchema]:
    """Return all product categories in the shop."""
    categories = await get_categories(db)
    return [CategoryReadSchema.model_validate(c) for c in categories]
