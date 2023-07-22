from typing import AsyncGenerator
from dataclasses import dataclass
from datetime import timedelta
import pytest
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.database import get_test_session
from src.pomodoro.utils import PomodoroSettingRepo, PomodoroHistoryRepo
from src.pomodoro.schemas import (
    CreatePomodoroSetting,
    UpdatePomodoroSetting,
    UpdatePomodoroHistory,
    ReadPomodoroSetting,
    CreatePomodoroHistory,
)
from src.pomodoro.utils import PomodoroHistory
from src.pomodoro.constants import PomodoroBaseEnum
from tests.auth.utils import MockDbUserManager


@dataclass
class PomodoroSettingsTestHolder:
    session: AsyncSession
    setting_repo: PomodoroSettingRepo
    user: User
    example_create_schema: CreatePomodoroSetting


@dataclass
class PomodoroHistoryTestHolder:
    session: AsyncSession
    repo: PomodoroHistoryRepo
    user: User
    base_setting: ReadPomodoroSetting
    base_history_create_schema: CreatePomodoroHistory
    created_record: PomodoroHistory


@asynccontextmanager
async def pomodoro_settings() -> AsyncGenerator[PomodoroSettingsTestHolder, None]:
    async with get_test_session() as session:
        user_manager = MockDbUserManager(session)

        pomodoro_setting_repo = PomodoroSettingRepo(session)
        user = await user_manager.get(1)
        example_create_schema = CreatePomodoroSetting(
            user_id=user.id,
            long_rest=50,
            short_rest=60,
            work_time=40,
            iterations=3,
        )
        result_to_yield = PomodoroSettingsTestHolder(
            session=session,
            setting_repo=pomodoro_setting_repo,
            user=user,
            example_create_schema=example_create_schema,
        )
        yield result_to_yield


@asynccontextmanager
async def pomodoro_history() -> AsyncGenerator[PomodoroHistoryTestHolder, None]:
    async with get_test_session() as session:
        user_manager = MockDbUserManager(session)
        history_repo = PomodoroHistoryRepo(session)
        setting_repo = PomodoroSettingRepo(session)

        user = await user_manager.get(1)
        base_setting = await setting_repo.create(CreatePomodoroSetting(user_id=user.id))
        base_history_create_schema = CreatePomodoroHistory(
            pomodoro_setting_id=base_setting.id
        )
        created_record = await history_repo.create(base_history_create_schema)
        result_to_yield = PomodoroHistoryTestHolder(
            session=session,
            repo=history_repo,
            user=user,
            base_setting=base_setting,
            base_history_create_schema=base_history_create_schema,
            created_record=created_record,
        )
        yield result_to_yield


@pytest.mark.asyncio
class TestPomodoroSetting:
    async def test_crete_pomodoro_setting(self):
        async with pomodoro_settings() as setting:
            result = await setting.setting_repo.create(setting.example_create_schema)
            outputed_schema = CreatePomodoroSetting(**result.dict())
        assert outputed_schema == setting.example_create_schema

    async def test_read_not_existent_settings(self):
        async with pomodoro_settings() as setting:
            result = await setting.setting_repo.read(setting.user.id)

        assert (
            result.iterations == PomodoroBaseEnum.ITERATIONS.value
            and result.long_rest == PomodoroBaseEnum.LONG_REST.value
            and result.short_rest == PomodoroBaseEnum.SHORT_REST.value
            and result.work_time == PomodoroBaseEnum.WORK.value
        )

    async def test_clear_schema(self):
        async with pomodoro_settings() as setting:
            _ = await setting.setting_repo.create(setting.example_create_schema)
            read_after_creation = await setting.setting_repo.read(setting.user.id)
            cleared_schema = await setting.setting_repo.clear(setting.user.id)
            read_after_clearing = await setting.setting_repo.read(setting.user.id)
        assert read_after_clearing != read_after_creation
        assert cleared_schema == read_after_clearing

    async def test_update_schema(self):
        async with pomodoro_settings() as setting:
            empty_update_schema = UpdatePomodoroSetting(user_id=setting.user.id)
            new_schema = await setting.setting_repo.create(
                setting.example_create_schema
            )
            updated_schema = await setting.setting_repo.update(empty_update_schema)

        assert new_schema != updated_schema

    async def test_create_with_cursed_user_id(self):
        async with pomodoro_settings() as setting:
            cursed_create_schema = CreatePomodoroSetting(user_id=-1)
            with pytest.raises(KeyError) as e_info:
                _ = await setting.setting_repo.create(cursed_create_schema)


@pytest.mark.asyncio
class TestHistory:
    async def test_creation_of_default_history(self):
        async with pomodoro_history() as setting:
            empty_history_schema = setting.base_history_create_schema
            new_history = await setting.repo.create(empty_history_schema)
        assert (
            empty_history_schema.created == new_history.created
            and empty_history_schema.updated == new_history.updated
            and empty_history_schema.pomodoro_setting_id
            == new_history.pomodoro_setting_id
        )

    async def test_read_of_created_record(self):
        async with pomodoro_history() as setting:
            created_record = setting.created_record
            read_schema = await setting.repo.read(created_record.id)
        assert created_record == read_schema

    async def test_update_record(self):
        async with pomodoro_history() as setting:
            created_record = setting.created_record
            custom_update = UpdatePomodoroHistory(
                id=created_record.id,
                created=setting.created_record.created - timedelta(days=2),
                updated=setting.created_record.updated,
            )
            updated_record = await setting.repo.update(custom_update)
        assert created_record != updated_record
        created_record.created = created_record.created - timedelta(days=2)
        assert created_record == updated_record

    async def test_delete_record(self):
        async with pomodoro_history() as setting:
            deleted_result = await setting.repo.delete(setting.created_record.id)
            with pytest.raises(KeyError) as e_info:
                _ = await setting.repo.read(setting.created_record.id)
        assert deleted_result == setting.created_record.id
