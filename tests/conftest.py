from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core import settings
from app.db.session import AsyncSessionLocal, engine
from app.main import app

assert str(settings.DB_URL).endswith("_test"), " Use `make test`."


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """One session per test, rolled back afterwards,add savepoint for commit user."""
    async with engine.connect() as connection:
        transaction = await connection.begin()
        async with AsyncSessionLocal(
            bind=connection,
            join_transaction_mode="create_savepoint",
        ) as session:
            yield session
        await transaction.rollback()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTP client that calls the app in-process, on the test's session."""
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
async def persist(db_session: AsyncSession):
    """Save objects built by the factories."""

    async def _persist(*objects):
        db_session.add_all(objects)
        await db_session.flush()
        return objects

    return _persist
