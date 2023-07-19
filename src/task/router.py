from fastapi import APIRouter, Depends, HTTPException
from .dependencies import DepTaskRepo, DepTagRepo, DepM2MTaskTagRepo
from .schemas import (
    ReadTask,
    CreateTask,
    UpdateTask,
    ReadTag,
    CreateTag,
    UpdateTag,
    CreateTag2Task,
    DeleteTag2TaskOutput,
    DeleteTag2Task,
)
from src.auth import DepActiveCurUser, ReadUserInner, BaseRolesEnum, Authorizator

task_router = APIRouter(prefix="/task", tags=["MAIN"])


@task_router.post("", response_model=ReadTask)
async def create_task(
    new_task: CreateTask,
    repo: DepTaskRepo,
    cur_user: DepActiveCurUser,
):
    if new_task.user_id is None or Authorizator.can_control(cur_user, new_task.user_id):
        new_task.user_id = cur_user.id
    else:
        raise HTTPException(401)

    return await repo.create_schema_out(new_task)


@task_router.get("/{task_id}", response_model=ReadTask)
async def read_task(
    task_id: int,
    repo: DepTaskRepo,
    cur_user: DepActiveCurUser,
):
    task = await repo.read(task_id)
    if not Authorizator.can_read(cur_user, task.user_id):
        raise HTTPException(401)
    return task


@task_router.put("", response_model=ReadTask)
async def update_task(
    upd_task: UpdateTask,
    repo: DepTaskRepo,
    user: DepActiveCurUser,
):
    task_user_id = upd_task.user_id
    if task_user_id is None:
        task = await repo.read(upd_task.id)
        task_user_id = task.user_id
    if not Authorizator.can_control(user, task_user_id):
        raise HTTPException(401)
    return await repo.update_schema_out(upd_task)


@task_router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    repo: DepTaskRepo,
    user: DepActiveCurUser,
):
    task = await repo.read(task_id)
    if not Authorizator.can_control(user, task.user_id):
        raise HTTPException(401)
    return await repo.delete(task_id)


tag_router = APIRouter(prefix="/tag")


@tag_router.post("", response_model=ReadTag)
async def create_tag(
    new_tag: CreateTag,
    repo: DepTagRepo,
    cur_user: DepActiveCurUser,
):
    if new_tag.user_id is None or Authorizator.can_control(cur_user, new_tag.user_id):
        new_tag.user_id = cur_user.id
    else:
        raise HTTPException(401)
    out_schema = await repo.create_schema_out(new_tag)
    return out_schema


@tag_router.get("/{tag_id}", response_model=ReadTag)
async def read_tag(
    tag_id: int,
    repo: DepTagRepo,
    cur_user: DepActiveCurUser,
):
    tag = await repo.read(tag_id)
    if not Authorizator.can_read(cur_user, tag.user_id):
        raise HTTPException(401)
    return tag


@tag_router.put("", response_model=ReadTag)
async def update_tag(
    upd_tag: UpdateTag,
    repo: DepTagRepo,
    cur_user: DepActiveCurUser,
):
    tag_user_id = upd_tag.user_id
    if tag_user_id is None:
        tag = await repo.read(upd_tag.id)
        tag_user_id = tag.user_id
    if not Authorizator.can_control(cur_user, tag_user_id):
        raise HTTPException(401)
    return await repo.update_schema_out(upd_tag)


@tag_router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    repo: DepTagRepo,
    cur_user: DepActiveCurUser,
):
    tag = await repo.read(tag_id)
    if not Authorizator.can_control(cur_user, tag.user_id):
        raise HTTPException(401)
    return await repo.delete(tag_id)


router_m2m_task_2_tag = APIRouter(prefix="/m2m")


@router_m2m_task_2_tag.post("/task", response_model=CreateTag2Task)
async def create_tag2task(
    map_schema: CreateTag2Task,
    repo: DepM2MTaskTagRepo,
    cur_user: DepActiveCurUser,
):
    tags: list = []
    for tag_id in map_schema.tag_ids:
        buf_tag = await repo.tag_repo.read(tag_id)
        tags.append(buf_tag)

    for tag in tags:
        if not Authorizator.can_control(cur_user, tag.user_id):
            raise HTTPException(401)

    return await repo.m2m_with_task(map_schema)


@router_m2m_task_2_tag.delete("/task")
async def delete_tag2task(
    delete_schema: DeleteTag2Task,
    repo: DepM2MTaskTagRepo,
    cur_user: DepActiveCurUser,
):
    
    return await repo.delete_m2m_with_task(delete_schema)


@router_m2m_task_2_tag.get("/tasks")
async def get_tasks_by_tag_id(
    tag_id: int, repo: DepM2MTaskTagRepo, cur_user: DepActiveCurUser
):
    return await repo.get_tasks(tag_id)


@router_m2m_task_2_tag.get("/tags")
async def get_tags_by_task_id(
    task_id: int, repo: DepM2MTaskTagRepo, cur_user: DepActiveCurUser
):
    return await repo.get_tags(task_id)


tag_router.include_router(router_m2m_task_2_tag)
