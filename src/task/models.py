from typing import List
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.mixins import TimeMixin
from src.database import Base
from src.auth.models import User
from src.pomodoro.models import PomodoroSetting

# M2M_task_to_tag = Table(
#     "task_2_tag",
#     Base.metadata,
#     Column("tag_id", ForeignKey("tag.id"), primary_key=True),
#     Column("task_id", ForeignKey("task.id"), primary_key=True),
# )


class Priority(Base):
    __tablename__ = "priority"

    code_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    number: Mapped[int] = mapped_column(unique=True, nullable=False)
    task_objs: Mapped[List["Task"]] = relationship(back_populates="priority_obj")


class M2MTask2Tag(Base):
    __tablename__ = "task_to_tag"
    __table_args__ = (UniqueConstraint("task_id", "tag_id"),)
    task_id: Mapped[int] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"), nullable=False, index=True
    )


class Task(Base, TimeMixin):
    __tablename__ = "task"
    name: Mapped[str] = mapped_column(default="", nullable=False)
    description: Mapped[str] = mapped_column(default="", nullable=False)
    deadline: Mapped[datetime] = mapped_column(
        DateTime(True), nullable=True, default=None
    )
    finished: Mapped[datetime] = mapped_column(
        DateTime(True), default=None, nullable=True
    )
    is_project: Mapped[bool] = mapped_column(nullable=False, default=False)
    priority_id: Mapped[int] = mapped_column(
        ForeignKey(Priority.id), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE"), nullable=False, index=True
    )
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("task.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
        index=True,
    )
    pomodoro_id: Mapped[int] = mapped_column(
        ForeignKey(PomodoroSetting.id), nullable=True, index=True, default=None
    )

    parent_obj: Mapped["Task"] = relationship()
    child_objs: Mapped[List["Task"]] = relationship()

    user_obj: Mapped[User] = relationship()
    priority_obj: Mapped[Priority] = relationship(back_populates="task_objs")

    # tag_objs: Mapped[List["Tag"]] = relationship(
    #     secondary=M2MTask2Tag, back_populates="task_objs"
    # )


class Tag(Base):
    __tablename__ = "tag"
    __table_args__ = (UniqueConstraint("user_id", "name"),)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    description: Mapped[str] = mapped_column(nullable=False, default="")

    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE"), nullable=False, index=True
    )
    # task_objs: Mapped[List[Task]] = relationship(
    #     secondary=M2MTask2Tag, back_populates="tag_objs"
    # )
