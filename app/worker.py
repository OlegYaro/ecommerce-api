import asyncio
from contextlib import asynccontextmanager
from functools import wraps

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.db.session import AsyncSessionLocal

celery_app = Celery("ecommerce", broker=settings.REDIS_URL, include=["app.tasks.order"])
celery_app.conf.update(
    task_ignore_result=True,
    task_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)


class _State:
    """Class to hold the state of the worker process."""

    loop = None
    engine = None
    session = None


state = _State()


@worker_process_init.connect
def _init(**_):
    """Initialize the worker process with a new event loop and database engine."""
    state.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(state.loop)
    state.engine = create_async_engine(
        str(settings.DB_URL), pool_size=1, max_overflow=1, pool_pre_ping=True
    )
    state.session = async_sessionmaker(
        state.engine, expire_on_commit=False, autoflush=False
    )


@worker_process_shutdown.connect
def _shutdown(**_):
    """Shutdown the worker process by disposing engine and closing event loop."""
    if state.loop:
        state.loop.run_until_complete(state.engine.dispose())
        state.loop.close()


@asynccontextmanager
async def db():
    """Provide an asynchronous database session for tasks."""
    async with (state.session or AsyncSessionLocal)() as session:
        yield session


def async_task(**options):
    """Decorator to run an async function as a Celery task."""

    def decorator(fn):
        @wraps(fn)
        def run(*args, **kwargs):
            coro = fn(*args, **kwargs)
            if state.loop:
                return state.loop.run_until_complete(coro)
            return asyncio.run(coro)

        return celery_app.task(**options)(run)

    return decorator
