from fastapi import APIRouter

from app.api.deps import DbSession
from app.schemas import CategoryReadSchema
from app.services import get_categories_service

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
async def list_categories(db: DbSession) -> list[CategoryReadSchema]:
    """Return all product categories in the shop."""
    return await get_categories_service(db)
