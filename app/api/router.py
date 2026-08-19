from fastapi import APIRouter

from app.api.category import router as category_router
from app.api.product import router as product_router
from app.api.user import router as user_router

api_router = APIRouter()
api_router.include_router(category_router)
api_router.include_router(product_router)
api_router.include_router(user_router)
