from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

# TODO Merge some optional parameters in update and create schemas of task table
class CreateTask(BaseModel):
    name: str
    description: str = ""
    priority_id: int
    is_project: bool = False
    user_id: Optional[int] = None
    parent_id: Optional[int] = None
    pomodoro_id: Optional[int] = None
    deadline: Optional[datetime] = None
    finished: Optional[datetime] = None


class ReadTask(CreateTask):
    id: int


class UpdateTask(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    priority_id: Optional[int] = None
    user_id: Optional[int] = None
    parent_id: Optional[int] = None
    pomodoro_id: Optional[int] = None
    is_project: Optional[bool] = None
    deadline: Optional[datetime] = None
    finished: Optional[datetime] = None
    


class CreateTag(BaseModel):
    name: str
    description: str = ""
    user_id: Optional[int] = None


class ReadTag(CreateTag):
    id: int


class UpdateTag(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None


class CreateTag2Task(BaseModel):
    task_ids: List[int]
    tag_ids: List[int]

class DeleteTag2Task(BaseModel):
    task_ids: Optional[List[int]] = None
    tag_ids: Optional[List[int]] = None


class DeleteTag2TaskOutput(BaseModel):
    task_id: int
    tag_id: int