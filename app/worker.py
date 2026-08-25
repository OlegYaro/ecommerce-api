import asyncio

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app.core.config import settings


class CeleryDB:
    """Class to hold the database state for Celery workers."""

    engine: AsyncEngine | None = None
    SessionLocal: async_sessionmaker | None = None
    loop: asyncio.AbstractEventLoop | None = None


db_state = CeleryDB()

celery_app = Celery(
    "ecommerce",
    broker=settings.REDIS_URL,
    include=["app.tasks.order"],
)

celery_app.conf.update(
    task_ignore_result=True,
    task_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    broker_connection_retry_on_startup=True,
)


@worker_process_init.connect
def init_worker_db(**kwargs):
    """Initialize connection and event loop when the worker process starts."""
    db_state.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(db_state.loop)

    db_state.engine = create_async_engine(
        str(settings.DB_URL), pool_pre_ping=True, pool_size=3, max_overflow=10
    )
    db_state.SessionLocal = async_sessionmaker(
        db_state.engine, expire_on_commit=False, autoflush=False
    )


@worker_process_shutdown.connect
def shutdown_worker_db(**kwargs):
    """Clean up resources when the worker process shuts down."""
    if db_state.engine and db_state.loop:
        db_state.loop.run_until_complete(db_state.engine.dispose())
    if db_state.loop:
        db_state.loop.close()
