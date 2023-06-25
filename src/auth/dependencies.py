from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.dependencies import dep_get_async_db_session
from .utils import AuthenticateRepo


async def get_repo(
    session: AsyncSession = Depends(dep_get_async_db_session),
) -> AuthenticateRepo:
    yield AuthenticateRepo(session)
