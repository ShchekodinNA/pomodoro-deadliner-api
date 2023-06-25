from typing import List
from src.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserRole(Base):
    __tablename__ = "user_role"

    code_name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="user_role")


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_pswd: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    user_role_id: Mapped[int] = mapped_column(
        ForeignKey(UserRole.id, ondelete="SET NULL"), nullable=True, index=True
    )
    user_role: Mapped["UserRole"] = relationship(back_populates="users")
