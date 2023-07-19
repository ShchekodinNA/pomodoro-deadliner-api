from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.mixins import TimeMixin
from src.auth.models import User
from .constants import PomodoroBaseEnum


class PomodoroSetting(Base):
    __tablename__ = "pomodoro_setting"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE"), nullable=False, index=True, unique=True
    )
    long_rest: Mapped[int] = mapped_column(
        nullable=False, default=PomodoroBaseEnum.LONG_REST.value
    )
    short_rest: Mapped[int] = mapped_column(
        nullable=False, default=PomodoroBaseEnum.SHORT_REST.value
    )
    work_time: Mapped[int] = mapped_column(
        nullable=False, default=PomodoroBaseEnum.WORK.value
    )
    iterations: Mapped[int] = mapped_column(
        nullable=False, default=PomodoroBaseEnum.ITERATIONS.value
    )

    user_obj: Mapped[User] = relationship()


class PomodoroHistory(Base, TimeMixin):
    __tablename__ = "pomodoro_history"

    pomodoro_setting_id: Mapped[int] = mapped_column(
        ForeignKey(PomodoroSetting.id, ondelete="CASCADE"), nullable=False, index=True
    )
    
