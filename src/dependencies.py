from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session  # as dep_get_async_db_session



async def dep_get_async_db_session() -> AsyncSession:
    async for session in get_session():
        yield session


DepAsyncDbSession = Annotated[AsyncSession, Depends(dep_get_async_db_session)]