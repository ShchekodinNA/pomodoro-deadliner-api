from src.database import get_session  # as dep_get_async_db_session
from sqlalchemy.ext.asyncio import AsyncSession


async def dep_get_async_db_session() -> AsyncSession:
    async for session in get_session():
        yield session
