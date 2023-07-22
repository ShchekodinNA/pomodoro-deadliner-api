from typing import Annotated
from fastapi import Depends
from src.dependencies import DepAsyncDbSession
from .utils import PomodoroHistoryRepo, PomodoroSettingRepo


async def get_pomodoro_history_repo(
    session: DepAsyncDbSession,
) -> PomodoroHistoryRepo:
    yield PomodoroHistoryRepo(session)


async def get_pomodoro_setting_repo(session: DepAsyncDbSession) -> PomodoroSettingRepo:
    yield PomodoroSettingRepo(session)


DepPomodoroHistoryRepo = Annotated[
    PomodoroHistoryRepo, Depends(get_pomodoro_history_repo)
]

DepPomodoroSettingRepo = Annotated[
    PomodoroSettingRepo, Depends(get_pomodoro_setting_repo)
]
