from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core import settings

engine = create_async_engine(
    settings.DB_URL, pool_pre_ping=True, pool_size=3, max_overflow=10
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
