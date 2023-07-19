import asyncio
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from pydantic import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DEBUG_MODE: str

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)
async_database_url = settings.ASYNC_DATABASE_URL
sync_database_url = settings.SYNC_DATABASE_URL
if settings.DEBUG_MODE is True:
    print(f"{async_database_url=}")


def async_session_generator():
    return sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=True,
        autocommit=False,
        expire_on_commit=False,
    )


async def get_session() -> AsyncSession:
    async_session = async_session_generator()
    async with async_session() as session:
        yield session
        await session.commit()


@asynccontextmanager
async def get_test_session() -> AsyncSession:
    async_sesion = async_session_generator()
    async with async_sesion() as session:
        try:
            yield session
        except Exception as exc:
            raise Exception() from exc
        finally:
            await session.rollback()
            await session.commit()


# class BaseWithoutID(DeclarativeBase):
#     pass


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
