from typing import List
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.mixins import TimeMixin, date_column_filler
from src.database import Base
from src.auth.models import User


class Priority(Base):
    __tablename__ = "priority"

    code_name: Mapped[str] = mapped_column(unique=True, nullable=False)

    task_objs: Mapped[List["Task"]] = relationship(back_populates="priority_obj")


class Task2Tag(Base):
    __tablename__ = "task_to_tag"
    __table_args__ = (UniqueConstraint("task_id", "tag_id"),)
    task_id: Mapped[int] = mapped_column(
        ForeignKey("task.id"), nullable=False, index=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id"), nullable=False, index=True
    )


class Task(Base, TimeMixin):
    __tablename__ = "task"
    name: Mapped[str] = mapped_column(default="", nullable=False)
    description: Mapped[str] = mapped_column(default="", nullable=False)
    deadline: Mapped[datetime] = date_column_filler
    finished: Mapped[datetime] = mapped_column(
        DateTime(True), default=datetime.utcnow()
    )
    is_project: Mapped[bool] = mapped_column(nullable=False, default=False)
    priority_id: Mapped[int] = mapped_column(
        ForeignKey(Priority.id, ondelete="SET NULL"), nullable=False, index=True
    )

    priority_obj: Mapped[Priority] = relationship(back_populates="task_objs")

    tag_objs: Mapped[List["Tag"]] = relationship(
        secondary=Task2Tag, back_populates="task_objs"
    )


class Tag(Base):
    __tablename__ = "tag"
    __table_args__ = (UniqueConstraint("user_id", "name"),)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    description: Mapped[str] = mapped_column(nullable=False, default="")

    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE"), nullable=False, index=True
    )
    task_objs: Mapped[List[Task]] = relationship(
        secondary=Task2Tag, back_populates="tag_objs"
    )
