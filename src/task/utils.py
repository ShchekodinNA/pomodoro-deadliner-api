from typing import List
from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql._typing import ColumnExpressionArgument
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
    DeleteTag2Task,
    DeleteTag2TaskOutput,
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
        db_tag = await self.read_obj(id_)
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
    def __init__(
        self, session: AsyncSession, tag_repo: TagRepo, task_repo: TaskRepo
    ) -> None:
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

    async def delete_m2m_with_task(
        self, delete_schema: DeleteTag2Task
    ) -> list[DeleteTag2TaskOutput]:
        stmt = delete(M2MTask2Tag)
        if delete_schema.tag_ids is None and delete_schema.task_ids is None:
            raise HTTPException(422, detail="Pass one of fields")
        if delete_schema.tag_ids is not None:
            stmt = stmt.where(M2MTask2Tag.tag_id.in_(delete_schema.tag_ids))
        if delete_schema.task_ids is not None:
            stmt = stmt.where(M2MTask2Tag.task_id.in_(delete_schema.task_ids))
        stmt = stmt.returning(M2MTask2Tag.tag_id, M2MTask2Tag.task_id)
        result = await self._execute(stmt)
        items = result.all()
        result_list = []
        for item in items:
            result_list.append(
                DeleteTag2TaskOutput(tag_id=item.t[0], task_id=item.t[1])
            )

        return result_list

    async def get_tasks(self, tag_id: int) -> List[ReadTask]:
        stmt = select(Task).join(M2MTask2Tag).where(M2MTask2Tag.tag_id == tag_id)
        result = await self._exexute_with_scalar_return(stmt)
        result_list = [self.get_read_shchema(item, ReadTask) for item in result]
        return result_list

    async def get_tags(self, task_id: int) -> List[ReadTag]:
        stmt = select(Tag).join(M2MTask2Tag).where(M2MTask2Tag.task_id == task_id)
        result = await self._exexute_with_scalar_return(stmt)
        result_list = [self.get_read_shchema(item, ReadTag) for item in result]
        return result_list
