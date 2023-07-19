from datetime import datetime
from typing import Optional, TypeAlias
from pydantic import BaseModel, Field
from src.mixins import TimeMixinForSchema
from .constants import PomodoroBaseEnum

field_long_rest = Field(PomodoroBaseEnum.LONG_REST.value, gt=0, le=120)
field_short_rest = Field(PomodoroBaseEnum.SHORT_REST.value, gt=0, le=120)
field_work_time = Field(PomodoroBaseEnum.WORK.value, gt=0, le=120)
field_iterations = Field(PomodoroBaseEnum.ITERATIONS.value, gt=0, le=12)


class CreatePomodoroSetting(BaseModel):
    user_id: int
    long_rest: Optional[int] = field_long_rest
    short_rest: Optional[int] = field_short_rest
    work_time: Optional[int] = field_work_time
    iterations: Optional[int] = field_iterations


class UpdatePomodoroSetting(CreatePomodoroSetting):
    pass


class ReadPomodoroSetting(CreatePomodoroSetting):
    id: int


class CreatePomodoroHistory(TimeMixinForSchema, BaseModel):
    pomodoro_setting_id: int


class UpdatePomodoroHistory(TimeMixinForSchema, BaseModel):
    id: int
    pomodoro_setting_id: Optional[int]


class ReadPomodoroHistory(UpdatePomodoroHistory):
    pass
