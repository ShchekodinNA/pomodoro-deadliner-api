from src.base_repo import IAsyncRepo
from sqlalchemy import select, delete
from .schemas import (
    CreatePomodoroHistory,
    CreatePomodoroSetting,
    ReadPomodoroHistory,
    ReadPomodoroSetting,
    UpdatePomodoroSetting,
    UpdatePomodoroHistory,
)
from .models import PomodoroHistory, PomodoroSetting


class PomodoroSettingRepo(IAsyncRepo):
    async def create(self, setting: CreatePomodoroSetting) -> ReadPomodoroSetting:
        db_setting = await self.create_obj(setting)
        output_schema = self.get_read_shchema(db_setting, ReadPomodoroSetting)
        return output_schema

    async def create_obj(self, setting: CreatePomodoroSetting) -> PomodoroSetting:
        db_setting = PomodoroSetting(**setting.dict())
        await self._add(db_setting)
        return db_setting

    async def read(self, user_id: int) -> ReadPomodoroSetting:
        db_obj = await self.read_obj(user_id)
        output_shema = self.get_read_shchema(db_obj, ReadPomodoroSetting)
        return output_shema

    async def read_obj(self, user_id: int) -> PomodoroSetting:
        stmt = select(PomodoroSetting).where(PomodoroSetting.user_id == user_id)
        try:
            db_obj = await self._get_one_record(stmt, PomodoroSetting)
        except KeyError:
            base_pomodoro_setting = CreatePomodoroSetting(user_id=user_id)
            db_obj = await self.create_obj(base_pomodoro_setting)
        return db_obj

    async def update(self, setting: UpdatePomodoroSetting) -> ReadPomodoroSetting:
        setting_obj = await self.read_obj(setting.user_id)
        setting_obj = await self._update(setting_obj, setting)
        output_schema = self.get_read_shchema(setting_obj, ReadPomodoroSetting)
        return output_schema

    async def clear(self, user_id) -> int:
        update_schema = UpdatePomodoroSetting(user_id=user_id)
        updated_result = await self.update(update_schema)
        return updated_result


class PomodoroHistoryRepo(IAsyncRepo):
    async def create(self, history: CreatePomodoroHistory) -> ReadPomodoroHistory:
        db_history = PomodoroHistory(**history.dict())
        output_schema = await self._add_schema_out(db_history, ReadPomodoroHistory)
        return output_schema
    
    async def read(self, id_) -> ReadPomodoroHistory:
        db_object = await self._get(PomodoroHistory, id_)
        output_schema = self.get_read_shchema(db_object, ReadPomodoroHistory)
        return output_schema

    async def update(self, update_history: UpdatePomodoroHistory) -> ReadPomodoroHistory:
        history_obj = await self._get(PomodoroHistory, update_history.id)
        history_obj = await self._update(history_obj, update_history)
        output_schema = self.get_read_shchema(history_obj, ReadPomodoroHistory)
        return output_schema

    async def delete(self, id_:int) -> int:
        deleted_id = await self._delete(PomodoroHistory, id_)
        return deleted_id