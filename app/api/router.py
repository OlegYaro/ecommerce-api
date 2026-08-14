from fastapi import APIRouter

from app.api import category_router, product_router

api_router = APIRouter()
api_router.include_router(category_router)
api_router.include_router(product_router)
