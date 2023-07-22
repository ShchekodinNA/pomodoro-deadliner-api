from fastapi import APIRouter, HTTPException
from .dependencies import DepPomodoroHistoryRepo, DepPomodoroSettingRepo
from .schemas import (
    ReadPomodoroHistory,
    CreatePomodoroHistory,
    UpdatePomodoroHistory,
    ReadPomodoroSetting,
    CreatePomodoroSetting,
    UpdatePomodoroSetting,
)
from src.auth import DepActiveCurUser, Authorizator

pomodoro_router = APIRouter(prefix="/pomodoro", tags=["POMODORO"])

_setting_router = APIRouter(prefix="/setting")


@_setting_router.post("", response_model=ReadPomodoroSetting)
async def create_pomodoro_setting(
    pomodoro_create: CreatePomodoroSetting,
    repo: DepPomodoroSettingRepo,
    user: DepActiveCurUser,
):
    if not Authorizator.can_control(user, pomodoro_create.user_id):
        raise HTTPException(401)
    try:
        setting = await repo.create(pomodoro_create)
    except KeyError as er:
        raise HTTPException(422, detail=er.args) from er
    return setting


@_setting_router.put("", response_model=ReadPomodoroSetting)
async def update_pomodoro_setting(
    pomdoro_upd: UpdatePomodoroSetting,
    repo: DepPomodoroSettingRepo,
    user: DepActiveCurUser,
):
    if not Authorizator.can_control(user, pomdoro_upd.user_id):
        raise HTTPException(401)
    try:
        setting = await repo.update(pomdoro_upd)
    except KeyError as er:
        raise HTTPException(422, detail=er.args) from er
    return setting


@_setting_router.get("/{user_id}", response_model=ReadPomodoroSetting)
async def get_pomodoro_setting(
    user_id: int, repo: DepPomodoroSettingRepo, user: DepActiveCurUser
):
    if not Authorizator.can_read(user, user_id):
        raise HTTPException(401)
    try:
        setting = await repo.read(user_id)
    except KeyError as er:
        raise HTTPException(422, detail=er.args) from er
    return setting


@_setting_router.delete("/{user_id}", response_model=ReadPomodoroSetting)
async def clear_pomodoro_setting(
    user_id: int, repo: DepPomodoroSettingRepo, user: DepActiveCurUser
):
    if not Authorizator.can_control(user, user_id):
        raise HTTPException(401)
    try:
        setting = await repo.clear(user_id)
    except KeyError as er:
        raise HTTPException(422, detail=er.args) from er
    return setting


_history_router = APIRouter(prefix="/history")


@_history_router.post("", response_model=ReadPomodoroHistory)
async def create_history(
    history: CreatePomodoroHistory,
    repo: DepPomodoroHistoryRepo,
    setting_repo: DepPomodoroSettingRepo,
    user: DepActiveCurUser,
):
    setting = await setting_repo.read(user.id)
    if history.pomodoro_setting_id != setting.id:
        if not Authorizator.can_control(user, -1):
            raise HTTPException(401)
    try:
        read_history = await repo.create(history)
    except KeyError as err:
        raise HTTPException(422, detail=err.args) from err
    return read_history


@_history_router.put("", response_model=ReadPomodoroHistory)
async def update_history(
    history: UpdatePomodoroHistory,
    repo: DepPomodoroHistoryRepo,
    setting_repo: DepPomodoroSettingRepo,
    user: DepActiveCurUser,
):
    setting = await setting_repo.read(user.id)
    if history.pomodoro_setting_id != setting.id:
        if not Authorizator.can_control(user, -1):
            raise HTTPException(401)
    try:
        updated_history = await repo.update(history)
    except KeyError as err:
        raise HTTPException(422, detail=err.args) from err
    return updated_history


@_history_router.get("{history_id}")
async def get_history_record(
    history_id: int,
    repo: DepPomodoroHistoryRepo,
    setting_repo: DepPomodoroSettingRepo,
    user: DepActiveCurUser,
):
    try:
        setting = await setting_repo.read(user.id)
        history = await repo.read(history_id)
        if history.pomodoro_setting_id != setting.id:
            if not Authorizator.can_control(user, -1):
                raise HTTPException(401)
        found_history = await repo.read(history_id)
    except KeyError as err:
        raise HTTPException(422, detail=err.args) from err
    return found_history


@_history_router.delete("{history_id}")
async def delete_history_record(
    history_id: int,
    repo: DepPomodoroHistoryRepo,
    setting_repo: DepPomodoroSettingRepo,
    user: DepActiveCurUser,
):
    try:
        setting = await setting_repo.read(user.id)
        history = await repo.read(history_id)
        if history.pomodoro_setting_id != setting.id:
            if not Authorizator.can_control(user, -1):
                raise HTTPException(401)
        deleted_result = await repo.delete(history_id)
    except KeyError as err:
        raise HTTPException(422, detail=err.args) from err
    return deleted_result


pomodoro_router.include_router(_setting_router)
pomodoro_router.include_router(_history_router)
