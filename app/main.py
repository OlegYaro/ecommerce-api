from fastapi import FastAPI
from sqlalchemy import text

from app.api import DbSession, api_router

app = FastAPI()

app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health_check(db: DbSession) -> dict:
    """Health check endpoint to verify if the application and database are running."""
    await db.execute(text("SELECT 1"))
    return {"status": "healthy", "database": "healthy"}
