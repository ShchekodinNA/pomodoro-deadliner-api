from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.base_repo import IAsyncRepo
from src.utils import union_keys_for_m2m
from .schemas import (
    CreateTask,
    ReadTask,
    UpdateTask,
    CreateTag,
    ReadTag,
    UpdateTag,
    CreateTag2Task,
)
from .models import Task, Tag, M2MTask2Tag

class TaskRepo(IAsyncRepo):
    async def create_schema_out(self, task: CreateTask) -> ReadTask:
        db_task = Task(**task.dict())
        return await self._add_schema_out(db_task, ReadTask)

    async def read(self, id_: int) -> ReadTask:
        db_task = await self._get(Task, id_)
        return self.get_read_shchema(db_task, ReadTask)

    async def update_schema_out(self, upd_task: UpdateTask) -> ReadTask:
        db_task = await self._update_by(Task, upd_task)
        return self.get_read_shchema(db_task, ReadTask)

    async def delete(self, id_: int) -> int:
        return await self._delete(Task, id_)


class TagRepo(IAsyncRepo):
    async def create_schema_out(self, tag: CreateTag) -> ReadTag:
        db_tag = Tag(**tag.dict())
        return await self._add_schema_out(db_tag, ReadTag)

    async def read(self, id_: int) -> ReadTag:
        db_tag = self.read_obj(id_)
        schema = self.get_read_shchema(db_tag, ReadTag)
        return schema

    async def read_obj(self, id_: int) -> Tag:
        db_tag = await self._get(Tag, id_)
        return db_tag

    async def update_schema_out(self, upd_tag: UpdateTag) -> ReadTag:
        db_tag = await self._update_by(Tag, upd_tag)
        return self.get_read_shchema(db_tag, ReadTag)

    async def delete(self, id_: int) -> int:
        return await self._delete(Tag, id_)

    # async def create_m2m_with_tag(self, m2m_schema: CreateTag2Task) -> CreateTag2Task:



class M2MTaskTagRepo(IAsyncRepo):
    def __init__(self, session: AsyncSession, tag_repo: TagRepo, task_repo: TaskRepo) -> None:
        super().__init__(session)
        self.tag_repo: TagRepo = tag_repo
        self.task_repo: TaskRepo = task_repo
    
    async def m2m_with_task(self, m2m_schema: CreateTag2Task) -> CreateTag2Task:
        instances = []
        for item in union_keys_for_m2m(m2m_schema.task_ids, m2m_schema.tag_ids):
            new_m2m = M2MTask2Tag(task_id=item[0], tag_id=item[1])
            instances.append(new_m2m)
        try:
            await self._add(*instances)
        except KeyError as err:
            raise HTTPException(status_code=422, detail=err.args) from err
        return m2m_schema