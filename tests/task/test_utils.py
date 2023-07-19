from typing import AsyncGenerator
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_test_session
from src.task.utils import M2MTaskTagRepo, TagRepo, TaskRepo
from src.task.schemas import CreateTag2Task, DeleteTag2Task
from src.task.models import M2MTask2Tag, Task, Tag
from src.auth.models import User
from tests.utils import SessionFor_testing
from .utils import (
    UniteManagerOfTaskTestModule,
)
from contextlib import asynccontextmanager

from dataclasses import dataclass


@dataclass
class M2MTestFixtureHolder:
    sesion: AsyncSession
    tag_repo: TagRepo
    task_repo: TaskRepo
    m2m_repo: M2MTaskTagRepo
    user: User
    tag1: Tag
    tag2: Tag
    tag3: Tag
    task1: Task
    task2: Task
    task3: Task
    task1_to_tag1: M2MTask2Tag
    task1_to_tag2: M2MTask2Tag
    task3_to_tag2: M2MTask2Tag
    task2_to_tag3: M2MTask2Tag


# @pytest.fixture(scope='session')
@asynccontextmanager
async def task_test_fixture() -> AsyncGenerator[M2MTestFixtureHolder, None]:
    async with get_test_session() as session:
        tag_repo = TagRepo(session)
        task_repo = TaskRepo(session)
        m2m_repo = M2MTaskTagRepo(session, tag_repo, task_repo)
        obj_manager = UniteManagerOfTaskTestModule(session)
        user = await obj_manager.user_manager.get(1)
        tag1 = await obj_manager.tag_manager.get(1, user_obj=user)
        tag2 = await obj_manager.tag_manager.get(2, user_obj=user)
        tag3 = await obj_manager.tag_manager.get(3, user_obj=user)
        task1 = await obj_manager.task_manager.get(1, user_obj=user)
        task2 = await obj_manager.task_manager.get(2, user_obj=user)
        task3 = await obj_manager.task_manager.get(3, user_obj=user)

        task1_to_tag1 = await obj_manager.tag_to_task_manager.get(
            1, tag_obj=tag1, task_obj=task1
        )
        task1_to_tag2 = await obj_manager.tag_to_task_manager.get(
            2, tag_obj=tag2, task_obj=task1
        )
        task3_to_tag2 = await obj_manager.tag_to_task_manager.get(
            3, tag_obj=tag2, task_obj=task3
        )
        task2_to_tag3 = await obj_manager.tag_to_task_manager.get(
            4, tag_obj=tag3, task_obj=task2
        )

        result_to_yield = M2MTestFixtureHolder(
            session,
            tag_repo,
            task_repo,
            m2m_repo,
            user,
            tag1,
            tag2,
            tag3,
            task1,
            task2,
            task3,
            task1_to_tag1,
            task1_to_tag2,
            task3_to_tag2,
            task2_to_tag3,
        )
        yield result_to_yield


@pytest.mark.asyncio
class TestHolder:
    async def test_deleting_m2m_task_tag(self):
        async with task_test_fixture() as task_test:
            deleting_objects = DeleteTag2Task(
                task_ids=[task_test.task1.id], tag_ids=[task_test.tag1.id]
            )
            deleted_objects = await task_test.m2m_repo.delete_m2m_with_task(
                deleting_objects
            )
        assert len(deleted_objects) == 1
        assert deleted_objects[0].tag_id == task_test.tag1.id
        assert deleted_objects[0].task_id == task_test.task1.id

    async def test_multiple_rows_delete(self):
        async with task_test_fixture() as task_test:
            deleted_objects = await task_test.m2m_repo.delete_m2m_with_task(
                DeleteTag2Task(task_ids=[task_test.task1.id])
            )
        assert len(deleted_objects) == 2
        for object_ in deleted_objects:
            assert object_.task_id == task_test.task1.id
            assert (
                object_.tag_id == task_test.tag1.id
                or object_.tag_id == task_test.tag2.id
            )

    async def test_getitng_tasks_by_tag_id(self):
        async with task_test_fixture() as task_test:
            id_to_check = [task_test.task1.id, task_test.task3.id]
            found_tasks = await task_test.m2m_repo.get_tasks(task_test.tag2.id)
        assert len(found_tasks) == 2
        for task in found_tasks:
            assert task.id in id_to_check

    async def test_getting_tags_by_task_id(self):
        async with task_test_fixture() as task_test:
            id_to_check = [task_test.tag1.id, task_test.tag2.id]
            tags = await task_test.m2m_repo.get_tags(task_test.task1.id)
        for tag in tags:
            assert tag.id in id_to_check
