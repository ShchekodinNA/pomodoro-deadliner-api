from typing import Annotated
from fastapi import Depends

# from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import DepAsyncDbSession
from .utils import TagRepo, TaskRepo, M2MTaskTagRepo


async def get_task_repo(
    session: DepAsyncDbSession,
) -> TaskRepo:
    yield TaskRepo(session)


async def get_tag_repo(
    session: DepAsyncDbSession,
) -> TagRepo:
    yield TagRepo(session)


async def get_m2m_tag_task_repo(session: DepAsyncDbSession) -> M2MTaskTagRepo:
    tag_repo = TagRepo(session)
    task_repo = TaskRepo(session)
    m2m_repo = M2MTaskTagRepo(session, tag_repo, task_repo)
    yield m2m_repo


DepTaskRepo = Annotated[TaskRepo, Depends(get_task_repo)]
DepTagRepo = Annotated[TagRepo, Depends(get_tag_repo)]
DepM2MTaskTagRepo = Annotated[M2MTaskTagRepo, Depends(get_m2m_tag_task_repo)]
